import type { PageData } from './$types';
import { GeometriesRepository, type Geometry } from '$lib/repositories/geometries';

export const load: () => Promise<PageData> = async () => {
	try {
		const response = await GeometriesRepository.getAll();
		const geometries = Array.isArray(response) ? response : response.results || [];

		// Filtrer uniquement les géométries avec un model_url valide et un fichier 3D
		const validGeometries = geometries.filter((geom: Geometry) => {
			return (
				geom.model_url && (geom.model_url.includes('.glb') || geom.model_url.includes('.gltf'))
			);
		});

		console.log('Géométries valides trouvées:', validGeometries);

		return {
			geometries: validGeometries,
			error: undefined
		};
	} catch (error) {
		console.error('Erreur de chargement des géométries:', error);
		return {
			geometries: [],
			error: 'Impossible de charger les géométries'
		};
	}
};
