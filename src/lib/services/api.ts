import { base } from '$app/paths';
import { browser } from '$app/environment';
import { ENDPOINTS } from '$lib/config';

export interface GeometryItem {
	id: string;
	name: string;
	type: string;
	color: string;
	position: { x: number; y: number; z: number };
	rotation: { x: number; y: number; z: number };
	scale: { x: number; y: number; z: number };
	visible: boolean;
	model_url?: string;
	local_file_id?: string; // ID pour IndexedDB
}

const LOCAL_STORAGE_KEY = 'dv_threlte_geometries_v1';
const DB_NAME = 'dv_threlte_assets';
const STORE_NAME = 'models';

/** 🗄️ IndexedDB helper pour les fichiers volumineux (GLB) */
const dbPromise = browser ? new Promise<IDBDatabase>((resolve, reject) => {
	const request = indexedDB.open(DB_NAME, 1);
	request.onupgradeneeded = () => request.result.createObjectStore(STORE_NAME);
	request.onsuccess = () => resolve(request.result);
	request.onerror = () => reject(request.error);
}) : null;

async function saveFileToDB(id: string, file: File) {
	const db = await dbPromise;
	if (!db) return;
	return new Promise((resolve, reject) => {
		const tx = db.transaction(STORE_NAME, 'readwrite');
		tx.objectStore(STORE_NAME).put(file, id);
		tx.oncomplete = resolve;
		tx.onerror = reject;
	});
}

async function getFileFromDB(id: string): Promise<File | null> {
	const db = await dbPromise;
	if (!db) return null;
	return new Promise((resolve) => {
		const tx = db.transaction(STORE_NAME, 'readonly');
		const req = tx.objectStore(STORE_NAME).get(id);
		req.onsuccess = () => resolve(req.result);
		req.onerror = () => resolve(null);
	});
}

export const geometryService = {
	async getAll(): Promise<GeometryItem[]> {
		let serverGeometries: GeometryItem[] = [];

		// 1. Charger l'Écho Statique (DB Snapshot)
		try {
			const staticUrl = `${base}/data/geometries.json`.replace('//', '/');
			const response = await fetch(staticUrl);
			if (response.ok) {
				serverGeometries = await response.json();
			}
		} catch (e) { }

		// 2. LocalStorage et IndexedDB
		if (browser) {
			const localData = localStorage.getItem(LOCAL_STORAGE_KEY);
			let userGeometries: GeometryItem[] = localData ? JSON.parse(localData) : [];

			// Restaurer les liens ObjectURL pour les fichiers locaux
			for (const item of userGeometries) {
				if (item.local_file_id) {
					const file = await getFileFromDB(item.local_file_id);
					if (file) {
						item.model_url = URL.createObjectURL(file);
						console.log(`✅ [IndexedDB] Restauré: ${item.name} (${file.size} bytes)`);
					} else {
						console.warn(`❌ [IndexedDB] Fichier non trouvé pour: ${item.name} (ID: ${item.local_file_id})`);
					}
				}
			}

			const mergedMap = new Map();
			serverGeometries.forEach(g => mergedMap.set(g.id.toString(), g));
			userGeometries.forEach(g => mergedMap.set(g.id.toString(), g));

			const result = Array.from(mergedMap.values());
			if (!localData && result.length > 0) this.saveLocal(result);
			return result;
		}

		return serverGeometries;
	},

	saveLocal(items: GeometryItem[]) {
		if (browser) {
			// On nettoie les ObjectURLs avant de sauver pour pas polluer le JSON
			const cleanItems = items.map(p => ({
				...p,
				model_url: p.local_file_id ? '' : p.model_url
			}));
			localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(cleanItems));
		}
	},

	async save(formData: FormData, id?: string): Promise<GeometryItem> {
		try {
			let url = ENDPOINTS.GEOMETRIES;
			let method = 'POST';
			if (id) {
				url = `${url}${id}/`;
				method = 'PUT';
			}

			const response = await fetch(url, { method, body: formData });
			if (response.ok) {
				const result = await response.json();
				const all = await this.getAll();
				this.saveLocal(all);
				return result;
			}
		} catch (e) { }

		// Fallback LocalStorage + IndexedDB
		if (browser) {
			const items = await this.getAll();
			const data: any = {};

			formData.forEach((value, key) => {
				if (['position', 'rotation', 'scale'].includes(key)) {
					try { data[key] = JSON.parse(value as string); } catch (e) { data[key] = value; }
				} else if (value instanceof File) {
					data['_file'] = value;
				} else if (key === 'visible') {
					data['visible'] = value === 'true';
				} else {
					data[key] = value;
				}
			});

			let newItem: GeometryItem;
			const targetId = id || Date.now().toString();

			if (data._file) {
				const fileId = `file_${targetId}`;
				await saveFileToDB(fileId, data._file);
				data.local_file_id = fileId;
				data.model_url = URL.createObjectURL(data._file);
				// On ne touche pas à data.type car il est déjà 'gltf_model' ou 'image_plane' via le formulaire
				delete data._file;
			}

			if (id) {
				const index = items.findIndex(i => i.id == id);
				if (index !== -1) {
					newItem = { ...items[index], ...data, id };
					items[index] = newItem;
				} else {
					newItem = { ...data, id };
					items.push(newItem);
				}
			} else {
				newItem = {
					...data,
					id: targetId,
					visible: data.visible ?? true,
					position: data.position || { x: 0, y: 0, z: 0 },
					rotation: data.rotation || { x: 0, y: 0, z: 0 },
					scale: data.scale || { x: 1, y: 1, z: 1 }
				};
				items.push(newItem);
			}

			this.saveLocal(items);
			return newItem;
		}
		throw new Error('Save failed');
	},

	async delete(id: string): Promise<void> {
		try {
			const response = await fetch(`${ENDPOINTS.GEOMETRIES}${id}/`, { method: 'DELETE' });
			if (response.ok) {
				const items = (await this.getAll()).filter(i => i.id != id);
				this.saveLocal(items);
				return;
			}
		} catch (e) { }

		if (browser) {
			const items = (await this.getAll()).filter(i => i.id != id);
			this.saveLocal(items);
		}
	},

	exportScene() {
		if (!browser) return;
		const data = localStorage.getItem(LOCAL_STORAGE_KEY);
		if (!data) return;
		const blob = new Blob([data], { type: 'application/json' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `dv-scene-${new Date().toISOString().split('T')[0]}.json`;
		a.click();
		URL.revokeObjectURL(url);
	},

	async importScene(file: File): Promise<void> {
		if (!browser) return;
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = (e) => {
				try {
					const importedItems = JSON.parse(e.target?.result as string);
					if (Array.isArray(importedItems)) {
						const currentItems = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || '[]');
						const mergedMap = new Map();
						currentItems.forEach((item: any) => mergedMap.set(item.id.toString(), item));
						importedItems.forEach((item: any) => mergedMap.set(item.id.toString(), item));
						this.saveLocal(Array.from(mergedMap.values()));
						resolve();
					} else reject(new Error("Format invalide"));
				} catch (err) { reject(err); }
			};
			reader.readAsText(file);
		});
	}
};

export const api = {
	get: async <T>(url: string) => {
		try {
			const baseUrl = ENDPOINTS.GEOMETRIES.split('/api')[0];
			const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
			const response = await fetch(fullUrl);
			return (await response.json()) as T;
		} catch (e) { return null as any; }
	},
	delete: async (url: string) => {
		try {
			const baseUrl = ENDPOINTS.GEOMETRIES.split('/api')[0];
			const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
			const response = await fetch(fullUrl, { method: 'DELETE' });
			return await response.json();
		} catch (e) { return null; }
	}
};
