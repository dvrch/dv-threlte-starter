import { getCloudinaryAssetUrl } from './cloudinaryAssets';

export async function getWorkingAssetUrl(
    fileName: string,
    type: 'models' | 'textures'
): Promise<string> {
    if (!fileName) return '';

    // 1. Extract pure filename from ANY URL (Vercel, Cloudinary, etc.)
    // We want to handle paths like:
    // - https://vercel-storage.com/models/xxx.glb
    // - https://res.cloudinary.com/.../v12345/xxx.glb
    // - /models/xxx.glb
    let pureName = fileName;
    if (fileName.includes('/')) {
        pureName = fileName.split('/').pop() || fileName;
    }

    // Remove common Cloudinary/Vercel junk from the filename itself
    // Some uploads have public IDs with random suffix or versioning
    // We strip leading versions like v12345678/
    pureName = pureName.replace(/^v\d+[\/\-_]/, '');

    // Search logic: try several folders on Cloudinary
    const foldersToTry = [
        type === 'models' ? 'dv-threlte/models' : 'dv-threlte/textures',
        'dv-threlte/public',
        'dv-threlte' // some might be in the root of the folder
    ];

    for (const folder of foldersToTry) {
        const cloudinaryUrl = getCloudinaryAssetUrl(pureName, folder);
        try {
            const response = await fetch(cloudinaryUrl, { method: 'HEAD' });
            if (response.ok) return cloudinaryUrl;
        } catch (e) { }
    }

    // 2. Check local fallbacks (if Cloudinary fails)
    const localPaths =
        type === 'models'
            ? [`/models/${pureName}`, `/public/${pureName}`, `/${pureName}`]
            : [`/textures/${pureName}`, `/public/${pureName}`, `/${pureName}`];

    for (const path of localPaths) {
        try {
            const res = await fetch(path, { method: 'HEAD' });
            if (res.ok) return path;
        } catch (e) { }
    }

    // 3. Last chance: if we have a full URL originally, and it's not a broken Vercel link, try it
    if (fileName.startsWith('http') && !fileName.includes('vercel-storage.com')) {
        return fileName;
    }

    // 4. Default to the first Cloudinary attempt structure if all else fails
    return getCloudinaryAssetUrl(pureName, foldersToTry[0]);
}
