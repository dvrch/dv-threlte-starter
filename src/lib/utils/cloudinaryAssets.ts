export const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

export function getCloudinaryAssetUrl(relativePath: string): string {
	// Ensure the relativePath starts with a '/'
	const cleanedPath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
	return `${CLOUDINARY_BASE_URL}/${cleanedPath}`;
}

// Configure DRACOLoader for Draco-compressed models
// This will be used by Threlte's useGltf automatically
export const configureDracoLoader = () => {
	if (typeof window === 'undefined') return; // Only on client-side

	import('three/examples/jsm/loaders/DRACOLoader.js').then(({ DRACOLoader }) => {
		const dracoLoader = new DRACOLoader();
		dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

		// Make it available globally for Threlte
		(window as any).THREE = (window as any).THREE || {};
		(window as any).THREE.DRACOLoader = dracoLoader;
	});
};
