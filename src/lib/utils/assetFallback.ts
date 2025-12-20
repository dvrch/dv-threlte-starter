export async function getWorkingAssetUrl(fileName: string, type: 'models' | 'textures'): Promise<string> {
    const { getCloudinaryAssetUrl } = await import('./cloudinaryAssets');
    const cloudinaryUrl = getCloudinaryAssetUrl(fileName);

    try {
        const response = await fetch(cloudinaryUrl, { method: 'HEAD' });
        if (response.ok) {
            return cloudinaryUrl;
        }
    } catch (e) {
        console.warn(`Cloudinary check failed for ${fileName}, searching local fallbacks.`);
    }

    // Check various local paths
    const localPaths = type === 'models'
        ? [`/models/${fileName}`, `/public/${fileName}`, `/${fileName}`]
        : [`/textures/${fileName}`, `/public/${fileName}`, `/${fileName}`];

    for (const path of localPaths) {
        try {
            const res = await fetch(path, { method: 'HEAD' });
            if (res.ok) return path;
        } catch (e) { }
    }

    // Default to first guess if all fail
    return localPaths[0];
}
