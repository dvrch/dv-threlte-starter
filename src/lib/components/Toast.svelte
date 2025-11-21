
<script lang="ts">
  import { toasts, removeToast } from '$lib/stores/toasts';
</script>

<div class="toast-container">
  {#each $toasts as toast (toast.id)}
    <div
      class="toast toast-{toast.type}"
      onclick={() => removeToast(toast.id)}
      onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') removeToast(toast.id); }}
      role="button"
      tabindex="0"
    >
      {toast.message}
    </div>
  {/each}
</div>

<style>
  .toast-container {
    position: fixed;
    top: 1rem;
    right: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 9999;
  }

  .toast {
    padding: 1rem;
    border-radius: 0.25rem;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .toast-info {
    background-color: #3498db;
  }

  .toast-success {
    background-color: #2ecc71;
  }

  .toast-error {
    background-color: #e74c3c;
  }
</style>
