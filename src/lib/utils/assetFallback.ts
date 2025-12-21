import { getCloudinaryAssetUrl } from './cloudinaryAssets';

// Map for files that have been renamed or replaced but we still want to support old names
const ASSET_MAPPING: Record<string, string> = {
    'nissan.glb': 'nissan2.glb',
    'garden.glb': 'garden1.glb'
};

// Fallback chain for assets that might be missing in their new versions
const FALLBACK_CHAIN: Record<string, string[]> = {
    'nissan2.glb': ['nissan1.glb', 'nissan.glb'],
    'garden1.glb': ['garden.glb']
};

/**
 * Strategy:
 * 1. Priority check for local files (Fast).
 * 2. Try Cloudinary folders.
 * 3. Final local fallback.
 */
export async function getWorkingAssetUrl(
    fileName: string,
    type: 'models' | 'textures'
): Promise<string> {
    if (!fileName) return '';

    let pureName = fileName;
    if (fileName.includes('/')) {
        pureName = fileName.split('/').pop() || fileName;
    }
    pureName = pureName.replace(/^v\d+[\/\-_]/, '');

    // Apply mapping (e.g. nissan.glb -> nissan2.glb)
    if (ASSET_MAPPING[pureName.toLowerCase()]) {
        pureName = ASSET_MAPPING[pureName.toLowerCase()];
    }

    const namesToTry = [pureName, ...(FALLBACK_CHAIN[pureName.toLowerCase()] || [])];

    const checkLocal = async (name: string) => {
        const paths =
            type === 'models'
                ? [`/models/${name}`, `/public/${name}`, `/${name}`]
                : [`/textures/${name}`, `/public/${name}`, `/${name}`];

        for (const path of paths) {
            try {
                const res = await fetch(path, { method: 'HEAD' });
                if (res.ok) return path;
            } catch (e) { }
        }
        return null;
    };

    // 1. Try to find any of the candidate names locally first for large/important assets
    const prioritizeLocal = ['spaceship.glb', 'nissan2.glb', 'nissan1.glb', 'nissan.glb', 'garden1.glb', 'star.png', 'bibi.png'].includes(pureName.toLowerCase());

    if (prioritizeLocal) {
        for (const candidate of namesToTry) {
            const localPath = await checkLocal(candidate);
            if (localPath) return localPath;
        }
    }

    // 2. Try Cloudinary for all candidates
    const foldersToTry = [
        type === 'models' ? 'dv-threlte/models' : 'dv-threlte/textures',
        'dv-threlte/public',
        'dv-threlte'
    ];

    for (const candidate of namesToTry) {
        for (const folder of foldersToTry) {
            const cloudinaryUrl = getCloudinaryAssetUrl(candidate, folder);
            try {
                const response = await fetch(cloudinaryUrl, { method: 'HEAD' });
                if (response.ok) return cloudinaryUrl;
            } catch (e) { }
        }
    }

    // 3. Last resort local check for all candidates
    for (const candidate of namesToTry) {
        const localPath = await checkLocal(candidate);
        if (localPath) return localPath;
    }

    // 4. Default fallback to the first Cloudinary URL
    return getCloudinaryAssetUrl(pureName, foldersToTry[0]);
}
