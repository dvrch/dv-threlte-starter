import { getCloudinaryAssetUrl } from './cloudinaryAssets';

export async function getWorkingAssetUrl(
    fileName: string,
    type: 'models' | 'textures'
): Promise<string> {
    // 1. Extract pure filename if full URL is passed
    let pureName = fileName;
    if (fileName.includes('/')) {
        pureName = fileName.split('/').pop() || fileName;
    }
    // Strip version junk if any (v12345/filename)
    pureName = pureName.replace(/^v\d+[\/\-_]/, '');

    // 2. Try the primary intended Cloudinary folder
    const primaryFolder = type === 'models' ? 'dv-threlte/models' : 'dv-threlte/textures';
    const primaryUrl = getCloudinaryAssetUrl(pureName, primaryFolder);

    try {
        const response = await fetch(primaryUrl, { method: 'HEAD' });
        if (response.ok) return primaryUrl;
    } catch (e) {
        console.warn(`Primary Cloudinary check failed for ${pureName}`);
    }

    // 3. Try the secondary (fallback) Cloudinary folder 'dv-threlte/public'
    const secondaryUrl = getCloudinaryAssetUrl(pureName, 'dv-threlte/public');
    try {
        const response = await fetch(secondaryUrl, { method: 'HEAD' });
        if (response.ok) return secondaryUrl;
    } catch (e) { }

    // 4. Check local fallbacks
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

    // 5. Hard fallback to the primary guessed Cloudinary URL if even locals fail
    return primaryUrl;
}
