import { dev } from '$app/environment';

export const CONFIG = {
    API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    CLOUDINARY_CLOUD_NAME: import.meta.env.VITE_CLOUDINARY_CLOUD_NAME || 'drcok7moc',
    IS_DEV: dev,
};
// Backward compatibility for components using direct fetch
export const API_ENDPOINTS = {
    GEOMETRIES: `${CONFIG.API_URL}/api/geometries/`,
    TYPES: `${CONFIG.API_URL}/api/types/`,
    FILMS: `${CONFIG.API_URL}/api/films/`,
    UPLOAD_BLOB: `${CONFIG.API_URL}/api/upload-blob/`,
    HANDLE_UPLOAD: `${CONFIG.API_URL}/api/handle-upload/`
};
