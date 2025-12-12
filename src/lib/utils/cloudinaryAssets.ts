export const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

export function getCloudinaryAssetUrl(relativePath: string): string {
	// Ensure the relativePath starts with a '/'
	const cleanedPath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
	return `${CLOUDINARY_BASE_URL}/${cleanedPath}`;
}

// Simple DRACOLoader configuration for client-side use only
export const createDracoLoader = async () => {
	if (typeof window === 'undefined') return null;

	const { DRACOLoader } = await import('three/examples/jsm/loaders/DRACOLoader.js');
	const dracoLoader = new DRACOLoader();
	dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
	return dracoLoader;
};
