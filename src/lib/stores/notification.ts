import { writable } from 'svelte/store';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

type Notification = {
    show: boolean;
    message: string;
    type: NotificationType;
    timeout?: number;
};

function createNotificationStore() {
    const { subscribe, set, update } = writable<Notification>({
        show: false,
        message: '',
        type: ''
    });

    return {
        subscribe,
        show: (message: string, type: NotificationType, timeout: number = 3000) => {
            set({ show: true, message, type });
            const timer = setTimeout(() => {
                set({ show: false, message: '', type: 'info' });
            }, timeout);
            return () => clearTimeout(timer);
        },
        hide: () => set({ show: false, message: '', type: 'info' })
    };
}

export const notification = createNotificationStore();
