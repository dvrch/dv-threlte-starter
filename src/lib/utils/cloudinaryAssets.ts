import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

export function getCloudinaryAssetUrl(relativePath: string): string {
	// Ensure the relativePath starts with a '/'
	const cleanedPath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
	return `${CLOUDINARY_BASE_URL}/${cleanedPath}`;
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