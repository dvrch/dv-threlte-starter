import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_CLOUD_NAME = 'drcok7moc';

/**
 * Generates a Cloudinary URL.
 * It tries to be smart about the folder.
 * If no folder is provided, it defaults to trying the 'dv-threlte/models' (common for .glb)
 * or 'dv-threlte/public'.
 */
export function getCloudinaryAssetUrl(path: string, folder: string = 'dv-threlte/models'): string {
	// 1. Clean the path: remove leading slash and any Vercel/Cloudinary junk
	let filename = path;
	if (path.includes('/')) {
		filename = path.split('/').pop() || path;
	}

	// Remove version string if present (e.g., v123456789/)
	filename = filename.replace(/^v\d+\//, '');

	// 2. Determine asset type based on extension
	const isImage = /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(filename);
	const resourceType = isImage ? 'image' : 'raw';

	// If it's an image and no specific folder provided, maybe default to textures
	const targetFolder = (isImage && folder === 'dv-threlte/models') ? 'dv-threlte/textures' : folder;

	// 3. Construct URL (without versioning for maximum reliability on manually guessed paths)
	return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/${resourceType}/upload/${targetFolder}/${filename}`;
}

// Helper to extract nodes and materials from a raw GLTF result (simulating useGltf behavior)
export function buildSceneGraph(gltf: any) {
	const nodes: Record<string, any> = {};
	const materials: Record<string, any> = {};
	if (gltf.scene) {
		gltf.scene.traverse((obj: any) => {
			if (obj.name) nodes[obj.name] = obj;
			if (obj.material) {
				if (Array.isArray(obj.material)) {
					obj.material.forEach((m: any) => {
						if (m.name) materials[m.name] = m;
					});
				} else {
					if (obj.material.name) materials[obj.material.name] = obj.material;
				}
			}
		});
	}
	return { nodes, materials };
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