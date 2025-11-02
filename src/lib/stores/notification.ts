import { writable } from 'svelte/store';

type Notification = {
    show: boolean;
    message: string;
    type: 'success' | 'error' | '';
};

function createNotificationStore() {
    const { subscribe, set, update } = writable<Notification>({
        show: false,
        message: '',
        type: ''
    });

    return {
        subscribe,
        show: (message: string, type: 'success' | 'error') => {
            set({ show: true, message, type });
            setTimeout(() => {
                set({ show: false, message: '', type: '' });
            }, 3000);
        },
        hide: () => set({ show: false, message: '', type: '' })
    };
}

export const notification = createNotificationStore();
