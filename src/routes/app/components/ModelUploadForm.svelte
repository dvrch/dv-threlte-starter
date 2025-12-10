<script lang="ts">
	import { fade } from 'svelte/transition';
	import { notification } from '$lib/stores/notification';
	import { ENDPOINTS } from '$lib/config';

	let file: File | null = null;
	let isUploading = false;
	let isOpen = false;
	let error = '';
	let success = '';

	function toggleForm() {
		isOpen = !isOpen;
		if (!isOpen) {
			resetForm();
		}
	}

	function resetForm() {
		file = null;
		error = '';
		success = '';
		isUploading = false;
	}

	async function handleSubmit() {
		if (!file) {
			error = 'Veuillez sélectionner un fichier';
			notification.show(error, 'error');
			return;
		}

		if (!file.name.endsWith('.glb') && !file.name.endsWith('.gltf')) {
			error = 'Le fichier doit être au format .glb ou .gltf';
			notification.show(error, 'error');
			return;
		}

		isUploading = true;
		error = '';
		success = '';

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch(API_ENDPOINTS.UPLOAD_BLOB, {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.error || 'Upload failed');
			}

			const data = await response.json();
			success = 'Modèle uploadé avec succès !';
			notification.show(success, 'success');
			resetForm();
			setTimeout(() => toggleForm(), 2000);
		} catch (e) {
			const errorMessage = e instanceof Error ? e.message : 'Une erreur est survenue';
			error = errorMessage;
			notification.show(error, 'error');
		} finally {
			isUploading = false;
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
	<div
		class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
		transition:fade
	>
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
					<label class="block text-sm font-medium text-gray-700"> Fichier 3D (GLB/GLTF) </label>
					<input
						type="file"
						accept=".glb,.gltf"
						class="w-full p-2 border rounded"
						on:change={(e) => file = (e.target as HTMLInputElement).files?.[0] || null}
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
					disabled={isUploading}
				>
					{isUploading ? 'Upload en cours...' : 'Upload'}
				</button>
			</form>
		</div>
	</div>
{/if}
