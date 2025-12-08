import { dev } from '$app/environment';

export const CONFIG = {
    API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    CLOUDINARY_CLOUD_NAME: import.meta.env.VITE_CLOUDINARY_CLOUD_NAME || 'drcok7moc',
    IS_DEV: dev,
};
