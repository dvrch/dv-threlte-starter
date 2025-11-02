<script lang="ts">
    import { fade } from 'svelte/transition';
    import { notification } from '$lib/stores/notification';
</script>

<div class="notifications-container">
    {#if $notification.show}
        <div 
            class="notification {$notification.type}"
            transition:fade={{ duration: 300 }}
        >
            <span class="message">{$notification.message}</span>
        </div>
    {/if}
</div>

<style>
    .notifications-container {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        pointer-events: none;
    }

    .notification {
        padding: 12px 24px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        min-width: 200px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .success {
        background-color: #10B981;
    }

    .error {
        background-color: #EF4444;
    }

    .warning {
        background-color: #F59E0B;
    }

    .info {
        background-color: #3B82F6;
    }
</style>
