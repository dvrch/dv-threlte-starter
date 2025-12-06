// src/lib/config.js
export const API_BASE_URL = import.meta.env.PROD
	? 'https://dv-threlte-starter.vercel.app/api'
	: 'http://localhost:8000/api';

export const API_ENDPOINTS = {
	GEOMETRIES: `${API_BASE_URL}/geometries/`,
	TYPES: `${API_BASE_URL}/types/`,
	FILMS: `${API_BASE_URL}/films/`,
	UPLOAD_BLOB: `${API_BASE_URL}/upload-blob/`,
	HANDLE_UPLOAD: `${API_BASE_URL}/handle-upload/`
};
