import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_CLOUD_NAME = 'drcok7moc';
export const CLOUDINARY_FOLDER = 'dv-threlte/public';

export function getCloudinaryAssetUrl(path: string): string {
	// 1. Clean the path: remove leading slash and 'public/' prefix if present
	let cleanedPath = path.startsWith('/') ? path.substring(1) : path;
	if (cleanedPath.startsWith('public/')) {
		cleanedPath = cleanedPath.substring(7);
	}

	// 2. Determine asset type based on extension
	const isImage = /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(cleanedPath);
	const resourceType = isImage ? 'image' : 'raw';

	// 3. Construct URL
	return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/${resourceType}/upload/${CLOUDINARY_FOLDER}/${cleanedPath}`;
}

// Create and configure a GLTFLoader with DRACOLoader
export const dracoGltfLoader = (() => {
	if (typeof window === 'undefined') {
		// Return a dummy loader for SSR to prevent errors, it won't be used anyway
		return new GLTFLoader();
	}

	const gltfLoader = new GLTFLoader();
	const dracoLoader = new DRACOLoader();
	dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
	gltfLoader.setDRACOLoader(dracoLoader);
	return gltfLoader;
})();