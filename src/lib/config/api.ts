// Configuration de l'API en fonction de l'environnement

export function getApiBaseUrl(): string {
  // En développement (Vite)
  if (typeof window === 'undefined') {
    // SSR/Server-side: utiliser une variable d'environnement ou une URL de production
    return process.env.VITE_API_URL || process.env.PUBLIC_API_URL || 'https://your-django-api.com';
  }
  
  // Client-side: utiliser le domaine actuel pour les requêtes relatives
  return '';
}

export function getGeometriesApiUrl(baseUrl?: string): string {
  const base = baseUrl || getApiBaseUrl();
  if (base) {
    return `${base}/api/geometries/`;
  }
  return '/api/geometries/';
}

export function getTypesApiUrl(baseUrl?: string): string {
  const base = baseUrl || getApiBaseUrl();
  if (base) {
    return `${base}/api/types/`;
  }
  return '/api/types/';
}

export function getUploadBlobApiUrl(baseUrl?: string): string {
  const base = baseUrl || getApiBaseUrl();
  if (base) {
    return `${base}/api/upload-blob/`;
  }
  return '/api/upload-blob/';
}
