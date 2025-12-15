import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_CLOUD_NAME = 'drcok7moc';
export const CLOUDINARY_FOLDER = 'dv-threlte/public';

export function getCloudinaryAssetUrl(path: string): string {
	// 1. Clean the path: remove leading slash
	let cleanedPath = path.startsWith('/') ? path.substring(1) : path;

	// Remove common prefixes iteratively to handle cases like "public/assets/models/nissan.glb"
	// We want to strip 'public/', 'assets/', 'models/' from the start until none remain,
	// or be selective. Based on the user logs, "assets/nissan.glb" -> 404.
	// The target seems to be just the filename for some, or "public/filename".
	// Let's assume the Cloudinary folder 'dv-threlte/public' ALREADY contains the structure.
	// If the file is 'nissan.glb' in 'dv-threlte/public', the URL ends in .../dv-threlte/public/nissan.glb
	// If we pass 'assets/nissan.glb', we might get .../dv-threlte/public/assets/nissan.glb which might be wrong
	// if the assets are flat or differently organized.

	// Given the previous error: https://res.cloudinary.com/drcok7moc/raw/upload/dv-threlte/public/assets/nissan.glb 404
	// This implies 'assets/' IS in the URL but the file IS NOT there.
	// Most likely, the file is at .../dv-threlte/public/nissan.glb directly.

	// Aggressively strip common folder names from the start of the path
	cleanedPath = cleanedPath.replace(/^(public\/|assets\/|models\/)+/, '');

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