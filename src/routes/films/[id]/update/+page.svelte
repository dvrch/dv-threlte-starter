<script>
    import { FilmStore } from '../../../../film-store';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    // Runes : récupération des props
    let { data } = $props();

    // États réactifs
    let film = $state({});
    let name = $state('');
    let director = $state('');
    let description = $state('');
    let files = $state(null);
    let showInvalidMessage = $state(false);
    let errorMessage = $state('');
    let isLoading = $state(false);

    onMount(async () => {
        const filmId = data.id;
        const existingFilm = $FilmStore.find((f) => f.id == filmId);

        if (existingFilm) {
            film = existingFilm;
        } else {
            try {
                const response = await fetch(`/api/films/${filmId}/`);
                if (!response.ok) throw new Error('Film not found');
                film = await response.json();
            } catch (error) {
                console.error('Failed to fetch film data:', error);
                film = null;
            }
        }

        if (film) {
            name = film.name || '';
            director = film.director || '';
            description = film.description || '';
        }
    });

    const validFields = () => {
        return name.length > 4 && director.length > 4 && description.length > 10;
    };

    const handleSubmit = async () => {
        if (!validFields()) {
            errorMessage = 'Veuillez vérifier les champs du formulaire.';
            showInvalidMessage = true;
            return;
        }

        isLoading = true;
        showInvalidMessage = false;
        let imageUrl = film.image_url; // Start with the existing image URL

        try {
            // Étape 1 & 2: Si un nouveau fichier est sélectionné, le téléverser
            if (files && files.length > 0) {
                const fileToUpload = files[0];

                const presignedUrlResponse = await fetch('/api/handle-upload/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filename: fileToUpload.name }),
                });

                if (!presignedUrlResponse.ok) {
                    const errorBody = await presignedUrlResponse.json();
                    throw new Error(
                        `Erreur du serveur pour obtenir l'URL pré-signée: ${errorBody.error || presignedUrlResponse.statusText}`
                    );
                }
                const blobData = await presignedUrlResponse.json();

                const uploadResponse = await fetch(blobData.uploadUrl, {
                    method: 'PUT',
                    body: fileToUpload,
                    headers: { 'Content-Type': fileToUpload.type },
                });

                if (!uploadResponse.ok) {
                    throw new Error("Échec du téléversement du fichier sur le stockage blob.");
                }

                imageUrl = blobData.downloadUrl; // Update to the new URL
            }

            // Étape 3: Soumettre les données mises à jour à Django
            const filmData = new FormData();
            filmData.append('name', name);
            filmData.append('director', director);
            filmData.append('description', description);
            filmData.append('image_url', imageUrl); // Send the new or existing URL

            const endpoint = `/api/films/${film.id}/`;
            const filmResponse = await fetch(endpoint, {
                method: 'PATCH', // PATCH is better for partial updates
                body: filmData,
            });

            if (!filmResponse.ok) {
                throw new Error('Échec de la mise à jour des données du film: ' + filmResponse.statusText);
            }

            const responseData = await filmResponse.json();

            // Update the store
            FilmStore.update((films) => {
                const index = films.findIndex((f) => f.id === responseData.id);
                if (index !== -1) {
                    films[index] = responseData;
                }
                return films;
            });

            goto('/films/');
        } catch (error) {
            console.error('Une erreur est survenue durant le processus de mise à jour:', error);
            errorMessage = error.message;
            showInvalidMessage = true;
        } finally {
            isLoading = false;
        }
    };
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
        
            <button class="btn btn-primary" type="submit">Submit</button>
        </form>
    </div>

</div>
