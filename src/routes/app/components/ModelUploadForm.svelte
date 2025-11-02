<script lang="ts"></script>
    let isOpen = false;
<script lang="ts">
    import { fade } from 'svelte/transition';
    import { notification } from '$lib/stores/notification';
    
    let file: File | null = null;
    let isUploading = false;
    let showForm = false;

    async function handleSubmit() {
        if (!file) {
            notification.show('Please select a file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        isUploading = true;

        try {
            const response = await fetch('http://localhost:8000/api/upload-blob/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');
            
            const data = await response.json();
            notification.show('Model uploaded successfully!', 'success');
            file = null;
        } catch (error) {
            notification.show('Failed to upload model', 'error');
        } finally {
            isUploading = false;
        }
    }
</script>

<div class="fixed right-4 top-20 z-50">
    <button 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-2"
        on:click={() => showForm = !showForm}
    >
        {showForm ? 'Close Upload' : 'Upload Model'}
    </button>

    {#if showForm}
        <div 
            class="bg-white p-4 rounded shadow-lg"
            transition:fade={{ duration: 200 }}
        >
            <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                <div>
                    <label class="block text-gray-700 text-sm font-bold mb-2">
                        Select 3D Model (GLB/GLTF)
                    </label>
                    <input 
                        type="file" 
                        accept=".glb,.gltf"
                        on:change={(e) => file = e.target.files?.[0] || null}
                        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline"
                    />
                </div>
                <button 
                    type="submit" 
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full"
                    disabled={isUploading}
                >
                    {isUploading ? 'Uploading...' : 'Upload'}
                </button>
            </form>
        </div>
    {/if}
</div>

<style>
    input[type="file"] {
        cursor: pointer;
    }
    
    input[type="file"]::-webkit-file-upload-button {
        background: #e5e7eb;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        margin-right: 1rem;
        cursor: pointer;
        border: none;
    }
    
    input[type="file"]::-webkit-file-upload-button:hover {
        background: #d1d5db;
    }
</style>    function toggleForm() {
        isOpen = !isOpen;
        resetForm();
    }

    function resetForm() {
        file = null;
        error = '';
        success = '';
    }

    async function handleSubmit() {
        if (!file) {
            error = 'Veuillez sélectionner un fichier';
            return;
        }

        if (!file.name.endsWith('.glb') && !file.name.endsWith('.gltf')) {
            error = 'Le fichier doit être au format .glb ou .gltf';
            return;
        }

        uploading = true;
        error = '';
        success = '';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/upload-blob/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Erreur lors de l\'upload');
            }

            const data = await response.json();
            success = 'Modèle uploadé avec succès !';
            resetForm();
            setTimeout(() => toggleForm(), 2000);
        } catch (e) {
            error = e.message || 'Une erreur est survenue';
        } finally {
            uploading = false;
        }
    }
</script>

<button
    class="fixed bottom-4 right-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full shadow-lg"
    on:click={toggleForm}
>
    {isOpen ? 'Fermer' : 'Upload Modèle 3D'}
</button>

{#if isOpen}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl w-96 relative">
            <button
                class="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
                on:click={toggleForm}
            >
                ✕
            </button>
            
            <h2 class="text-xl font-bold mb-4">Upload de Modèle 3D</h2>
            
            <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700">
                        Fichier 3D (GLB/GLTF)
                    </label>
                    <input
                        type="file"
                        accept=".glb,.gltf"
                        class="w-full p-2 border rounded"
                        on:change={(e) => file = e.target.files?.[0] || null}
                    />
                </div>

                {#if error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/if}

                {#if success}
                    <p class="text-green-500 text-sm">{success}</p>
                {/if}

                <button
                    type="submit"
                    class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                    disabled={uploading}
                >
                    {uploading ? 'Upload en cours...' : 'Upload'}
                </button>
            </form>
        </div>
    </div>
{/if}
