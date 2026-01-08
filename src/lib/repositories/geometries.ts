import { geometryService, type GeometryItem as Geometry } from '../services/api';

export type { Geometry };

export const GeometriesRepository = {
    getAll: async () => {
        return geometryService.getAll();
    },

    delete: async (id: string) => {
        return geometryService.delete(id);
    },

    // Add create/update if needed
};
