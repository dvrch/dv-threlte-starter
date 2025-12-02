<script>
    import {FilmStore} from '../../../film-store'
    import {goto} from '$app/navigation';
    
    let name = $state('');
    let director = $state('');
    let description = $state('');
    let tags = $state('');
    let files = $state();
    let showInvalidMessage = $state(false);
    let errorMessage = $state('');
    let isLoading = $state(false);

    const validFields = $derived(() => {
        return name.length >= 1 && director.length >= 1 && description.length >= 1 && files && files.length > 0;
    });

    let handleSubmit = async () => {
        if (!validFields) {
            errorMessage = "Veuillez remplir tous les champs et sélectionner un fichier.";
            showInvalidMessage = true;
            return;
        }

        isLoading = true;
        showInvalidMessage = false;
        const fileToUpload = files[0];
        const formData = new FormData();
        formData.append('file', fileToUpload);

        try {
            // Étape 1: Upload vers Vercel Blob via notre backend
            const response = await fetch('/api/upload-blob/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Upload failed');
            }

            const data = await response.json();
            const finalBlobUrl = data.url;

            // Étape 2: Soumettre les données du film avec la nouvelle URL à Django
            const filmData = new FormData();
            filmData.append('name', name);
            filmData.append('director', director);
            filmData.append('description', description);
            filmData.append('image_url', finalBlobUrl);

            if (tags.length) {
                const tagList = tags.split(",");
                tagList.forEach(tag => filmData.append('tags', tag.trim()));
            }

            const filmEndpoint = '/api/films/';
            const filmResponse = await fetch(filmEndpoint, {
                method: 'POST',
                body: filmData
            });

            if (!filmResponse.ok) {
                throw new Error('Échec de la sauvegarde des données du film: ' + filmResponse.statusText);
            }

            const responseData = await filmResponse.json();
            FilmStore.update(prev => [...prev, responseData]);
            goto('/films/');

        } catch (error) {
            console.error('Une erreur est survenue durant le processus de téléversement:', error);
            errorMessage = error.message;
            showInvalidMessage = true;
        } finally {
            isLoading = false;
        }
    }
</script>


<div>

    <h2 class="my-4">Add a Film</h2>

    {#if showInvalidMessage }
        <h4 class="text-danger">Form data is not valid</h4>
    {/if }

    <div class="col-12 col-md-6">
        <form onsubmit={(event) => { event.preventDefault(); handleSubmit(); }}>
            <div class="mb-3">
                <input class="form-control" type="text" placeholder="name" bind:value={name}/>
            </div>
            <div class="mb-3">
                <input class="form-control" type="text" placeholder="director" bind:value={director}/>
            </div>
            <div class="mb-3">
                <input class="form-control" type="text" placeholder="description" bind:value={description}/>
            </div>
            <div class="mb-3">
                <input class="form-control" type="file" bind:files/>
            </div>
            <div class="mb-3">
                <input class="form-control" type="text" placeholder="tags" bind:value={tags}/>
            </div>
            <button class="btn btn-primary" type="submit">Submit</button>
        </form>
    </div>

</div>

