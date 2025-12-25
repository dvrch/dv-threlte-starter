import { getCloudinaryAssetUrl } from './cloudinaryAssets';

// Map for files that have been renamed or replaced but we still want to support old names
const ASSET_MAPPING: Record<string, string> = {
    'nissan.glb': 'nissan2.glb',
    'nissant.glb': 'nissan2.glb',
    'garden.glb': 'garden1.glb',
    'clothe_sim_rffdfn.glb': 'cloth_sim.glb'
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

    // 1. Try to find local files (Dev speed)
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

    // 1. Priority check for local files (Dev speed)
    const prioritizeLocal = ([] as string[]).includes(pureName.toLowerCase()); // Forced Cloudinary for major assets

    if (prioritizeLocal) {
        for (const candidate of namesToTry) {
            const path = await checkLocal(candidate);
            if (path) return path;
        }
    }

    // 2. CLOUDINARY (The new main storage)
    		const foldersToTry =
    			type === 'models'
    				? ['dv-threlte/models', 'dv-threlte/public', 'dv-threlte']
    				: ['dv-threlte/textures', 'dv-threlte/public', 'dv-threlte'];    for (const candidate of namesToTry) {
        for (const folder of foldersToTry) {
            const cloudinaryUrl = getCloudinaryAssetUrl(candidate, folder);
            try {
                const response = await fetch(cloudinaryUrl, { method: 'HEAD' });
                if (response.ok) return cloudinaryUrl;
            } catch (e) { }
        }
    }

    // 3. Last fallback local
    if (!prioritizeLocal) {
        for (const candidate of namesToTry) {
            const path = await checkLocal(candidate);
            if (path) return path;
        }
    }

    // 4. Default to Cloudinary even if HEAD failed (might be CORS or temporary)
    return getCloudinaryAssetUrl(pureName, foldersToTry[0]);
}
