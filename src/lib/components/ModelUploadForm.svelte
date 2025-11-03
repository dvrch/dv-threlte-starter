<script lang="ts">
    import { fade } from 'svelte/transition';
    import { notification } from '$lib/stores/notification';
    
    let file: File | null = null;
    let isUploading = false;
    let dragOver = false;

    function onFileChange(e: Event) {
        const input = e.target as HTMLInputElement;
        file = input.files?.[0] || null;
    }

    function handleDragOver(e: DragEvent) {
        e.preventDefault();
        dragOver = true;
    }

    function handleDragLeave() {
        dragOver = false;
    }

    function handleDrop(e: DragEvent) {
        e.preventDefault();
        dragOver = false;
        const droppedFile = e.dataTransfer?.files[0];
        if (droppedFile?.name.match(/\.(glb|gltf)$/i)) {
            file = droppedFile;
        } else {
            notification.show('Please drop a GLB or GLTF file', 'error');
        }
    }

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        if (!file) {
            notification.show('Please select a file', 'error');
            return;
        }

        isUploading = true;
        const formData = new FormData();
        formData.append('file', file);

        try {
            // 1) Upload vers Vercel Blob / stockage local (backend gère le fallback)
            const response = await fetch('http://localhost:8000/api/upload-blob/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Upload failed');
            }

            const data = await response.json();
            const modelType = file.name.split('.').pop()?.toLowerCase();

            notification.show('Model uploaded successfully!', 'success');

            // Émettre un événement global pour pré-remplir le formulaire AddGeometry
            window.dispatchEvent(new CustomEvent('modelUploaded', {
                detail: { url: data.url, filename: data.filename ?? file.name, model_type: modelType }
            }));
            // Demander au layout de basculer sur l'onglet Add
            window.dispatchEvent(new CustomEvent('app:switchTab', { detail: 'add' }));

            // Optionnel: créer directement une entrée Geometry avec model_url (décommenter si souhaité)
            // await fetch('http://localhost:8000/api/geometries/', {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify({
            //         name: data.filename ?? file.name,
            //         type: 'box',
            //         color: '#cccccc',
            //         position: { x: 0, y: 0, z: 0 },
            //         rotation: { x: 0, y: 0, z: 0 },
            //         model_url: data.url,
            //         model_type: modelType
            //     })
            // });

            // Notifier la scène d'une mise à jour possible
            window.dispatchEvent(new Event('modelAdded'));
            file = null;
        } catch (error) {
            console.error('Upload error:', error);
            notification.show(
                error instanceof Error ? error.message : 'Failed to upload model',
                'error'
            );
        } finally {
            isUploading = false;
        }
    }
</script>

<div 
    class="model-upload-container"
    role="region"
    class:drag-over={dragOver}
    on:dragover={handleDragOver}
    on:dragleave={handleDragLeave}
    on:drop={handleDrop}
>
    <h3 class="title">Upload 3D Model</h3>
    <div class="upload-area">
        <form on:submit|preventDefault={handleSubmit}>
            <div class="file-input-container">
                {#if file}
                    <div class="selected-file">
                        <span class="file-name">{file.name}</span>
                        <button 
                            type="button" 
                            class="clear-button"
                            on:click={() => file = null}
                        >
                            ×
                        </button>
                    </div>
                {:else}
                    <label class="file-label">
                        <input 
                            type="file" 
                            accept=".glb,.gltf"
                            on:change={onFileChange}
                        />
                        <span>Drop GLB/GLTF here<br>or click to browse</span>
                    </label>
                {/if}
            </div>
            <button 
                type="submit" 
                class="upload-button"
                disabled={!file || isUploading}
            >
                {#if isUploading}
                    <span class="loading"></span>
                    Uploading...
                {:else}
                    Upload Model
                {/if}
            </button>
        </form>
    </div>
</div>

<style>
    .model-upload-container {
        background: white;
        border-radius: 8px;
        padding: 16px;
        width: 300px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .model-upload-container.drag-over {
        background: #f0f9ff;
        border: 2px dashed #3b82f6;
    }

    .title {
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 16px;
        color: #1f2937;
    }

    .upload-area {
        border-radius: 6px;
        padding: 8px;
    }

    .file-input-container {
        margin-bottom: 16px;
    }

    .file-label {
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px dashed #e5e7eb;
        border-radius: 6px;
        padding: 24px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
    }

    .file-label:hover {
        border-color: #3b82f6;
        background: #f0f9ff;
    }

    .file-label input {
        display: none;
    }

    .selected-file {
        display: flex;
        align-items: center;
        background: #f3f4f6;
        padding: 8px 12px;
        border-radius: 6px;
    }

    .file-name {
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .clear-button {
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 0 4px;
        font-size: 1.2em;
    }

    .clear-button:hover {
        color: #ef4444;
    }

    .upload-button {
        width: 100%;
        background: #3b82f6;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: background-color 0.2s;
    }

    .upload-button:hover:not(:disabled) {
        background: #2563eb;
    }

    .upload-button:disabled {
        background: #9ca3af;
        cursor: not-allowed;
    }

    .loading {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
