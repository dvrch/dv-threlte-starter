import { GeometriesRepository, type Geometry } from '../repositories/geometries';

export async function findGeometryByName(partialName: string): Promise<Geometry | null> {
	try {
		const response = await GeometriesRepository.getAll();
		const geometries = Array.isArray(response) ? response : response.results || [];

		// Search for geometry by partial name match (case-insensitive)
		return (
			geometries.find((geom) => geom.name.toLowerCase().includes(partialName.toLowerCase())) || null
		);
	} catch (error) {
		console.error(`Failed to find geometry with name containing "${partialName}":`, error);
		return null;
	}
}

export async function findGeometryByType(type: string): Promise<Geometry | null> {
	try {
		const response = await GeometriesRepository.getAll();
		const geometries = Array.isArray(response) ? response : response.results || [];

		// Search for geometry by type match (case-insensitive)
		return geometries.find((geom) => geom.type.toLowerCase() === type.toLowerCase()) || null;
	} catch (error) {
		console.error(`Failed to find geometry with type "${type}":`, error);
		return null;
	}
}

export async function getModelUrlByName(partialName: string): Promise<string | null> {
	const geometry = await findGeometryByName(partialName);
	return geometry?.model_url || null;
}

export async function getModelUrlByType(type: string): Promise<string | null> {
	const geometry = await findGeometryByType(type);
	return geometry?.model_url || null;
}
