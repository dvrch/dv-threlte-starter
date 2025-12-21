import { getCloudinaryAssetUrl } from './cloudinaryAssets';

/**
 * Strategy:
 * 1. For very large files (e.g. spaceship.glb), force local.
 * 2. Try Cloudinary folders.
 * 3. Try local fallbacks based on file existence.
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

    // 🛡️ FORCE LOCAL FOR SPACESHIP (User request: size > 10MB)
    if (pureName.toLowerCase() === 'spaceship.glb') {
        return '/models/spaceship.glb';
    }

    const preferLocal = [
        'nissan.glb',
        'garden1.glb',
        'bibi3.glb',
        'bibi.png',
        'energy-beam-opacity.png'
    ].includes(pureName.toLowerCase());

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

    if (preferLocal) {
        const localPath = await checkLocal(pureName);
        if (localPath) return localPath;
    }

    // 2. Try Cloudinary folders
    const foldersToTry = [
        type === 'models' ? 'dv-threlte/models' : 'dv-threlte/textures',
        'dv-threlte/public',
        'dv-threlte'
    ];

    for (const folder of foldersToTry) {
        const cloudinaryUrl = getCloudinaryAssetUrl(pureName, folder);
        try {
            const response = await fetch(cloudinaryUrl, { method: 'HEAD' });
            if (response.ok) return cloudinaryUrl;
        } catch (e) { }
    }

    // 3. Secondary Local check (if not already checked or if preferLocal failed)
    if (!preferLocal) {
        const localPath = await checkLocal(pureName);
        if (localPath) return localPath;
    }

    // 4. Default to Cloudinary if all else fails
    return getCloudinaryAssetUrl(pureName, foldersToTry[0]);
}
