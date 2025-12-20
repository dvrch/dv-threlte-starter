import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import * as THREE from 'three';

export const CLOUDINARY_CLOUD_NAME = 'drcok7moc';

/**
 * Generates a Cloudinary URL.
 */
export function getCloudinaryAssetUrl(path: string, folder: string = 'dv-threlte/models'): string {
	let filename = path;
	if (path.includes('/')) {
		filename = path.split('/').pop() || path;
	}
	filename = filename.replace(/^v\d+[\/\-_]/, '');

	const isImage = /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(filename);
	const resourceType = isImage ? 'image' : 'raw';
	const targetFolder = (isImage && (folder === 'dv-threlte/models')) ? 'dv-threlte/textures' : folder;

	return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/${resourceType}/upload/${targetFolder}/${filename}`;
}

/**
 * Robust helper to extract nodes and materials from a raw GLTF result.
 * Uses Proxies to prevent "undefined" property access crashes during rendering.
 */
export function buildSceneGraph(gltf: any) {
	const nodes: Record<string, any> = {};
	const materials: Record<string, any> = {};

	// Create fallback objects to prevent Three.js core from crashing on missing materials/geometries
	const defaultMaterial = new THREE.MeshStandardMaterial({ color: 0x888888, name: 'fallback' });
	const defaultGeometry = new THREE.BufferGeometry();
	const dummyMesh = new THREE.Mesh(defaultGeometry, defaultMaterial);
	dummyMesh.name = 'node_fallback';

	if (gltf.scene) {
		gltf.scene.traverse((obj: any) => {
			if (obj.name) nodes[obj.name] = obj;
			if (obj.isMesh && obj.material) {
				const mats = Array.isArray(obj.material) ? (obj.material as THREE.Material[]) : [obj.material as THREE.Material];
				mats.forEach((m: THREE.Material) => {
					if (m.name) materials[m.name] = m;
				});
			}
		});
	}

	// Protection Proxy for materials: if material name is missing, return a grey placeholder
	const safeMaterials = new Proxy(materials, {
		get(target: any, prop: string | symbol) {
			if (typeof prop === 'string' && !target[prop]) {
				// If it's a known Threlte internal property (like $$typeof or similar), don't return a material
				if (prop.startsWith('_') || prop === 'constructor') return target[prop];
				return defaultMaterial;
			}
			return target[prop];
		}
	});

	// Protection Proxy for nodes: return a dummy Mesh if name is missing
	const safeNodes = new Proxy(nodes, {
		get(target: any, prop: string | symbol) {
			if (typeof prop === 'string' && !target[prop]) {
				if (prop.startsWith('_') || prop === 'constructor') return target[prop];
				return dummyMesh;
			}
			return target[prop];
		}
	});

	return { nodes: safeNodes, materials: safeMaterials };
}

// Create and configure a GLTFLoader with DRACOLoader
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