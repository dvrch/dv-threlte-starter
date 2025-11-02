<script>
    import {FilmStore} from '../../../film-store'
    import {goto} from '$app/navigation';
    
    let name = '';
    let director = '';
    let description = '';
    let tags = '';
    let files;
    let showInvalidMessage = false;
    let errorMessage = '';
    let isLoading = false;

    let validFields = () => {
        return name.length > 4 && director.length > 4 && description.length > 10 && files && files.length > 0;
    }

    let handleSubmit = async () => {
        if (!validFields()) {
            errorMessage = "Veuillez remplir tous les champs et sélectionner un fichier.";
            showInvalidMessage = true;
            return;
        }

        isLoading = true;
        showInvalidMessage = false;
        const fileToUpload = files[0];

        try {
            // Étape 1: Obtenir l'URL pré-signée depuis notre backend
            const presignedUrlResponse = await fetch('/api/handle-upload/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: fileToUpload.name }),
            });

            if (!presignedUrlResponse.ok) {
                const errorBody = await presignedUrlResponse.json();
                throw new Error(`Erreur du serveur pour obtenir l'URL pré-signée: ${errorBody.error || presignedUrlResponse.statusText}`);
            }
            const blobData = await presignedUrlResponse.json();

            // Étape 2: Téléverser le fichier directement sur Vercel Blob
            const uploadResponse = await fetch(blobData.uploadUrl, {
                method: 'PUT',
                body: fileToUpload,
                headers: {
                    // Certains stockages cloud nécessitent des en-têtes spécifiques, 
                    // Vercel Blob est souvent simple mais on peut ajouter le type de contenu.
                    'Content-Type': fileToUpload.type,
                }
            });

            if (!uploadResponse.ok) {
                throw new Error('Échec du téléversement du fichier sur le stockage blob.');
            }
            
            const finalBlobUrl = blobData.downloadUrl;

            // Étape 3: Soumettre les données du film avec la nouvelle URL à Django
            const filmData = new FormData();
            filmData.append('name', name);
            filmData.append('director', director);
            filmData.append('description', description);
            filmData.append('image_url', finalBlobUrl); // Utilise le nouveau champ et l'URL finale

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
        <form on:submit|preventDefault={handleSubmit}>
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

