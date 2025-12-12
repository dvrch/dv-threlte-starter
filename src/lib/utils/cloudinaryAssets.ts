import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

export function getCloudinaryAssetUrl(relativePath: string): string {
	// Ensure the relativePath starts with a '/'
	const cleanedPath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
	return `${CLOUDINARY_BASE_URL}/${cleanedPath}`;
}

export const dracoGltfLoader = new DRACOLoader();
dracoGltfLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
