import { api } from '../services/api';

export interface Geometry {
    id: string;
    position: { x: number; y: number; z: number };
    rotation: { x: number; y: number; z: number };
    type: string;
    color: string;
    name: string;
    model_url?: string;
}

export const GeometriesRepository = {
    getAll: async () => {
        return api.get<Geometry[] | { results: Geometry[] }>('api/geometries/');
    },

    delete: async (id: string) => {
        return api.delete(`api/geometries/${id}/`);
    },

    // Add create/update if needed
};
