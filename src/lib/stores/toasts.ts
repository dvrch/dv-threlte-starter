
import { writable } from 'svelte/store';

export const toasts = writable([]);

export const addToast = (message, type = 'info') => {
  const id = Math.random().toString(36).substr(2, 9);
  toasts.update(all => [...all, { id, message, type }]);
  setTimeout(() => removeToast(id), 3000);
};

export const removeToast = id => {
  toasts.update(all => all.filter(t => t.id !== id));
};
