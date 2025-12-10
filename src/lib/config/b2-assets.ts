// Configuration des URLs Backblaze B2 pour les assets
export const B2_BASE_URL = 'https://f003.backblazeb2.com/file/43dvcapp/';

// Mapping des assets vers leurs URLs B2
export const B2_ASSETS = {
	// Modèles 3D (GLB/GLTF)
	'nissan2.glb': `${B2_BASE_URL}nissan2.glb`,
	'Barrel Model1.glb': `${B2_BASE_URL}Barrel Model1.glb`,
	'Barrel Model+.glb': `${B2_BASE_URL}Barrel Model+.glb`,
	'cloth_sim.glb': `${B2_BASE_URL}cloth_sim.glb`,
	'bibi.glb': `${B2_BASE_URL}bibi.glb`,
	'bibi2.glb': `${B2_BASE_URL}bibi2.glb`,
	'bibi3.glb': `${B2_BASE_URL}bibi3.glb`,
	'cdn.glb': `${B2_BASE_URL}cdn.glb`,
	'DRAP+Barrel Model1.glb': `${B2_BASE_URL}DRAP+Barrel Model1.glb`,
	'mario.glb': `${B2_BASE_URL}mario.glb`,
	'peagh-drap.glb': `${B2_BASE_URL}peagh-drap.glb`,

	// Textures (PNG/JPG/WEBP)
	'bibi.png': `${B2_BASE_URL}bibi.png`,
	'tete2porc.png': `${B2_BASE_URL}tete2porc.png`,
	'mario.png': `${B2_BASE_URL}mario.png`,
	'zaki.png': `${B2_BASE_URL}zaki.png`,
	'Tout.jpg': `${B2_BASE_URL}Tout.jpg`,
	'diamond.jpg': `${B2_BASE_URL}diamond.jpg`,
	'hero-bg.jpg': `${B2_BASE_URL}hero-bg.jpg`,
	'hero-bg.webp': `${B2_BASE_URL}hero-bg.webp`,
	'diamond.webp': `${B2_BASE_URL}diamond.webp`
};

// Fonction utilitaire pour obtenir l'URL B2 d'un asset
export function getB2AssetUrl(assetName: string): string {
	return B2_ASSETS[assetName as keyof typeof B2_ASSETS] || `${B2_BASE_URL}${assetName}`;
}

// Fonction pour vérifier si un asset existe dans B2_ASSETS
export function hasB2Asset(assetName: string): boolean {
	return assetName in B2_ASSETS;
}

// Exporter la liste de tous les assets disponibles
export function listB2Assets(): string[] {
	return Object.keys(B2_ASSETS);
}
