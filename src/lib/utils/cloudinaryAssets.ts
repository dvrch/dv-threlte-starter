import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import * as THREE from 'three';

export const CLOUDINARY_CLOUD_NAME = 'drcok7moc';

/**
 * Generates a Cloudinary URL.
 */
export function getCloudinaryAssetUrl(filename: string, folder: string = "dv-threlte/models"): string {
	if (!filename) return "";
	if (filename.startsWith("http")) {
		// Clean existing URLs from version strings if present
		return filename.replace(/\/v\d+\//, '/');
	}

	const isImage = /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(filename);
	const resourceType = isImage ? "image" : "raw";
	const targetFolder = folder;

	return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/${resourceType}/upload/${targetFolder}/${filename}`;
}

/**
 * Robust helper to extract nodes and materials from a raw GLTF result.
 * It traverses ALL scenes and forces valid materials on every object to prevent Three.js crashes.
 */
export function buildSceneGraph(gltf: any) {
	const nodes: Record<string, any> = {};
	const materials: Record<string, any> = {};

	// 🛡️ THE ULTIMATE FALLBACK MATERIAL (Invisible but exists, avoids crashes)
	const defaultMaterial = new THREE.MeshStandardMaterial({
		color: 0xff00ff, // Bright PINK for debug visibility if it ever shows up
		name: 'PROTECTION_FALLBACK'
	});
	const defaultGeometry = new THREE.BufferGeometry();
	const dummyMesh = new THREE.Mesh(defaultGeometry, defaultMaterial);
	dummyMesh.name = 'PROTECTION_NODE';

	const allScenes = gltf.scenes || (gltf.scene ? [gltf.scene] : []);
	allScenes.forEach((scene: THREE.Group) => {
		scene.traverse((obj: any) => {
			if (obj.name) nodes[obj.name] = obj;

			// 🛡️ AGGRESSIVE REPAIR: Every renderable object MUST have a valid material
			if (obj.material !== undefined) {
				if (Array.isArray(obj.material)) {
					obj.material = obj.material.map((m: any) => m || defaultMaterial);
				} else if (!obj.material) {
					obj.material = defaultMaterial;
				}
			} else if (obj.isMesh || obj.isPoints || obj.isLine) {
				obj.material = defaultMaterial;
			}

			// Fill lookup tables for Svelte templates
			if (obj.material) {
				const mats = Array.isArray(obj.material) ? (obj.material as THREE.Material[]) : [obj.material as THREE.Material];
				mats.forEach((m: THREE.Material) => {
					if (m && m.name) {
						materials[m.name] = m;
					}
				});
			}

			if ((obj.isMesh || obj.isPoints || obj.isLine) && !obj.geometry) {
				obj.geometry = defaultGeometry;
			}
		});
	});

	// Protection Proxy for template material access (e.g. gltf.materials.Body)
	const safeMaterials = new Proxy(materials, {
		get(target: any, prop: string | symbol) {
			if (typeof prop === 'string' && !target[prop]) {
				if (prop.startsWith('_') || prop === 'constructor' || prop === '$$typeof') return target[prop];
				return defaultMaterial;
			}
			return target[prop as any];
		}
	});

	const safeNodes = new Proxy(nodes, {
		get(target: any, prop: string | symbol) {
			if (typeof prop === 'string' && !target[prop]) {
				if (prop.startsWith('_') || prop === 'constructor' || prop === '$$typeof') return target[prop];
				return dummyMesh;
			}
			return target[prop as any];
		}
	});

	return { nodes: safeNodes, materials: safeMaterials };
}

// Singleton loader with Draco support
export const dracoGltfLoader = (() => {
	if (typeof window === 'undefined') {
		return new GLTFLoader();
	}
	const gltfLoader = new GLTFLoader();
	const dracoLoader = new DRACOLoader();
	dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
	gltfLoader.setDRACOLoader(dracoLoader);
	return gltfLoader;
})();