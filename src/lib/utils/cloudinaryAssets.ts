import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

export const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

// Create a GLTFLoader instance with DRACOLoader configured
const createDracoGltfLoader = () => {
    const loader = new GLTFLoader();
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
    loader.setDRACOLoader(dracoLoader);
    return loader;
};

// Export a singleton instance of the configured loader
export const dracoGltfLoader = createDracoGltfLoader();

export function getCloudinaryAssetUrl(relativePath: string): string {
    // Ensure the relativePath starts with a '/'
    const cleanedPath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
    return `${CLOUDINARY_BASE_URL}/${cleanedPath}`;
}
