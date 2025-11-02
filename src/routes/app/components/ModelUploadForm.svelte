<script lang="ts"></script>
    let isOpen = false;
    let file: File | null = null;
    let uploading = false;
    let error = '';
    let success = '';

    function toggleForm() {
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
