<script>
    import { onMount } from 'svelte';
    import { ENDPOINTS } from '$lib/config';

    let b2Assets = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        try {
            const response = await fetch(ENDPOINTS.B2_ASSETS);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            b2Assets = data.results || [];
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });
</script>

<div class="container">
    <h2 class="my-4">Blackblaze B2 Assets</h2>

    {#if loading}
        <p>Loading B2 assets...</p>
    {:else if error}
        <p class="text-danger">Error: {error}</p>
    {:else if b2Assets.length === 0}
        <p>No B2 assets found.</p>
    {:else}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>File Name</th>
                        <th>Original Name</th>
                        <th>Bucket Name</th>
                        <th>Content Type</th>
                        <th>File Size</th>
                        <th>URL</th>
                        <th>Uploaded At</th>
                    </tr>
                </thead>
                <tbody>
                    {#each b2Assets as asset}
                        <tr>
                            <td>{asset.id}</td>
                            <td>{asset.file_name}</td>
                            <td>{asset.original_name || 'N/A'}</td>
                            <td>{asset.bucket_name}</td>
                            <td>{asset.content_type}</td>
                            <td>{asset.file_size ? (asset.file_size / 1024 / 1024).toFixed(2) + ' MB' : 'N/A'}</td>
                            <td><a href={asset.url} target="_blank" rel="noopener noreferrer">Link</a></td>
                            <td>{new Date(asset.created_at).toLocaleString()}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

<style>
    /* Add some basic styling if needed, or rely on global app.css */
</style>
