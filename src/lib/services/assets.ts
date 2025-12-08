import { CONFIG } from '../config';

type AssetType = 'image' | 'video' | 'raw' | 'auto';

class AssetService {
    private cloudName: string;
    private baseUrl: string;

    constructor() {
        this.cloudName = CONFIG.CLOUDINARY_CLOUD_NAME;
        this.baseUrl = `https://res.cloudinary.com/${this.cloudName}`;
    }

    /**
     * Génère l'URL d'un asset (Cloudinary en prod, Local en dev)
     * @param path Chemin de l'asset (ex: 'models/threlte.glb')
     * @param type Type de l'asset (image, video, raw, auto)
     */
    getUrl(path: string, type: AssetType = 'auto'): string {
        if (!path) return '';
        if (path.startsWith('http')) return path;

        // En Dev, on sert les fichiers locaux (si nécessaire)
        // MAIS ici on veut forcer Cloudinary si les assets ne sont plus en local
        // Si tu as supprimé les assets locaux, on doit utiliser Cloudinary même en dev.

        // Nettoyage du path
        const cleanPath = path.startsWith('/') ? path.slice(1) : path;

        // Construire l'URL Cloudinary
        // Structure: https://res.cloudinary.com/<cloud_name>/<resource_type>/upload/<version>/<public_id>
        // Note: On omet la version pour l'instant ou on utilise v1

        let resourceType = type;
        if (type === 'auto') {
            if (cleanPath.endsWith('.glb') || cleanPath.endsWith('.gltf') || cleanPath.endsWith('.bin')) {
                resourceType = 'raw';
            } else if (cleanPath.endsWith('.mp4') || cleanPath.endsWith('.webm')) {
                resourceType = 'video';
            } else {
                resourceType = 'image';
            }
        }

        // Dossier 'dv-threlte' ajouté lors de l'upload
        const publicId = `dv-threlte/${cleanPath}`;

        return `${this.baseUrl}/${resourceType}/upload/${publicId}`;
    }
}

export const assets = new AssetService();
