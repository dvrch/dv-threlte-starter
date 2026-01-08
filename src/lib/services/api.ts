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
}

const LOCAL_STORAGE_KEY = 'dv_threlte_geometries_v1';

export const geometryService = {
	async getAll(): Promise<GeometryItem[]> {
		// 1. Try to get from LocalStorage first if in browser (for user changes on static site)
		if (browser) {
			const localData = localStorage.getItem(LOCAL_STORAGE_KEY);
			if (localData) {
				console.log('📦 Loaded from LocalStorage');
				return JSON.parse(localData);
			}
		}

		// 2. Try to get from real API
		try {
			const response = await fetch(ENDPOINTS.GEOMETRIES, {
				headers: { Accept: 'application/json' }
			});
			if (response.ok) {
				const data = await response.json();
				const results = Array.isArray(data) ? data : (data.results || []);
				if (browser && results.length > 0) this.saveLocal(results); // Cache it
				return results;
			}
		} catch (e) {
			console.warn('⚠️ API Backend unreachable, falling back to static JSON');
		}

		// 3. Fallback to static snapshot (GitHub Pages context)
		try {
			const staticUrl = `${base}/data/geometries.json`;
			const response = await fetch(staticUrl);
			if (response.ok) {
				const data = await response.json();
				if (browser) this.saveLocal(data);
				return data;
			}
		} catch (e) {
			console.error('❌ Static snapshot not found');
		}

		return [];
	},

	saveLocal(items: GeometryItem[]) {
		if (browser) {
			localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(items));
		}
	},

	async save(formData: FormData, id?: string): Promise<GeometryItem> {
		// Try real API first
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
				// Refresh local cache after successful server save
				const all = await this.getAll();
				this.saveLocal(all);
				return result;
			}
		} catch (e) {
			console.warn('⚠️ Could not save to backend, using LocalStorage only');
		}

		// Local Fallback for GitHub Pages
		if (browser) {
			const items = await this.getAll();
			const data: any = {};

			// Extract data from FormData
			formData.forEach((value, key) => {
				if (key === 'position' || key === 'rotation' || key === 'scale') {
					try {
						data[key] = JSON.parse(value as string);
					} catch (e) {
						data[key] = value;
					}
				} else {
					data[key] = value;
				}
			});

			let newItem: GeometryItem;
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
					id: Date.now().toString(),
					visible: data.visible === 'true'
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
				// Remove from local cache
				const items = (await this.getAll()).filter(i => i.id != id);
				this.saveLocal(items);
				return;
			}
		} catch (e) {
			console.warn('⚠️ Backend delete failed, deleting locally');
		}

		if (browser) {
			const items = (await this.getAll()).filter(i => i.id != id);
			this.saveLocal(items);
		}
	}
};

// 🏁 Export pour la compatibilité avec d'autres parties du code
export const api = {
	get: async <T>(url: string) => {
		try {
			const baseUrl = ENDPOINTS.GEOMETRIES.split('/api')[0];
			const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
			const response = await fetch(fullUrl);
			return (await response.json()) as T;
		} catch (e) {
			console.error('API Get failed', e);
			return null as any;
		}
	},
	delete: async (url: string) => {
		try {
			const baseUrl = ENDPOINTS.GEOMETRIES.split('/api')[0];
			const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
			const response = await fetch(fullUrl, { method: 'DELETE' });
			return await response.json();
		} catch (e) {
			console.error('API Delete failed', e);
			return null;
		}
	}
};

