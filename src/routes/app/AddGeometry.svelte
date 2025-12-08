<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { addToast } from '$lib/stores/toasts';
	import { API_ENDPOINTS } from '$lib/config';

	const { selectedGeometry = null } = $props();

	$effect(() => {
		if (selectedGeometry && selectedGeometry.id !== selectedGeometryId) {
			loadGeometryDetails(selectedGeometry.id);
		}
	});

	const getRandomValue = (min: number, max: number) =>
		Number(Math.random() * (max - min) + min).toFixed(2);

	// State for the form (runes)
	let name = $state('');
	let type = $state('box');
	let color = $state(
		`#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`
	);
	let position = $state({ x: 0, y: 0, z: 0 });
	let rotation = $state({
		x: Number(getRandomValue(0, 360)),
		y: Number(getRandomValue(0, 360)),
		z: Number(getRandomValue(0, 360))
	});
	let file: File | null = $state(null); // State for the uploaded file

	let geometries = $state([]);
	let selectedGeometryId = $state('');
	let isEditing = $state(false);
	let types = $state([]);
	let isLoading = $state(false);

	const loadTypes = async () => {
		try {
			console.log('Fetching from:', API_ENDPOINTS.TYPES);
			const response = await fetch(API_ENDPOINTS.TYPES, {
				headers: { Accept: 'application/json' }
			});

			console.log('Response status (Types):', response.status);
			const text = await response.text();
			console.log('Response text (Types, first 500 chars):', text.substring(0, 500));

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${text}`);
			}

			const data = JSON.parse(text);
			console.log('Parsed data (Types):', data);

			if (Array.isArray(data)) {
				types = data.map((type) => type.id);
			} else {
				console.error('Expected array for types but got:', data);
				types = [];
			}
		} catch (error) {
			console.error('Error loading types:', error);
			addToast('Failed to load types. Please try again.', 'error');
		}
	};

	const dispatch = createEventDispatcher();

	const resetForm = () => {
		type = types.length > 0 ? types[Math.floor(Math.random() * types.length)] : 'box';
		name = type;
		color = `#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`;
		position = {
			x: Number(getRandomValue(-5, 5)),
			y: Number(getRandomValue(-5, 5)),
			z: Number(getRandomValue(-5, 5))
		};
		rotation = {
			x: Number(getRandomValue(0, 360)),
			y: Number(getRandomValue(0, 360)),
			z: Number(getRandomValue(0, 360))
		};
		isEditing = false;
		selectedGeometryId = '';
		file = null;
	};

	onMount(() => {
		(async () => {
			await loadTypes();
			await loadGeometries();
			resetForm();
		})();
	});

	const loadGeometries = async () => {
		try {
			console.log('Fetching from:', API_ENDPOINTS.GEOMETRIES);
			const response = await fetch(API_ENDPOINTS.GEOMETRIES, {
				headers: { Accept: 'application/json' }
			});

			console.log('Response status (Geometries):', response.status);
			const text = await response.text();
			console.log('Response text (Geometries, first 500 chars):', text.substring(0, 500));

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${text}`);
			}

			const data = JSON.parse(text);
			console.log('Parsed data (Geometries):', data);

			if (data.results && Array.isArray(data.results)) {
				geometries = data.results;
			} else if (Array.isArray(data)) {
				geometries = data;
			} else {
				console.error('Unexpected data format for geometries:', data);
				geometries = [];
			}
		} catch (error) {
			console.error('Error loading geometries:', error);
			addToast('Failed to load geometries. Please try again.', 'error');
		}
	};

	import { upload } from '@vercel/blob/client';

	const handleSubmit = async () => {
		isLoading = true;
		try {
			let modelUrl = '';

			// 1. Client-side Upload to Vercel Blob
			if (file) {
				const blob = await upload(file.name, file, {
					access: 'public',
					handleUploadUrl: '/api/upload'
				});
				modelUrl = blob.url;
				addToast('File uploaded to Blob!', 'success');
			}

			// 2. Submit Metadata to Django
			const randomId = Math.random().toString(36).substring(2, 7);
			const uniqueName = isEditing ? name : `${name || (file ? file.name : 'geo')}-${randomId}`;

			const geometryData = {
				name: uniqueName,
				type: type,
				color: color,
				position: position, // JSON automatically serialized
				rotation: rotation,
				model_url: modelUrl || undefined
			};

			// Si on edit et qu'on a pas changé le fichier, on ne met pas model_url (ou on garde l'ancien)
			// Mais ici on simplifie: si modelUrl est vide, le backend garde l'ancien si PATCH/PUT partiel?
			// Attention: pour PUT il faut tout envoyer. Pour PATCH c'est partiel.
			// Ici on utilise PUT pour update complet ou POST pour create.

			// Si c'est un upload de fichier, on force le type 'gltf_model' pour le backend
			if (file) {
				geometryData.type = 'gltf_model';
				const ext = file.name.split('.').pop()?.toLowerCase();
				if (ext) geometryData.model_type = ext;
			}

			let url = API_ENDPOINTS.GEOMETRIES;
			let method = 'POST';

			if (isEditing && selectedGeometryId) {
				url = `${url}${selectedGeometryId}/`;
				method = 'PUT'; // Ou PATCH si on veut
			}

			// Envoi JSON uniquement ! Plus de FormData pour le fichier vers Django
			const response = await fetch(url, {
				method,
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify(geometryData)
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.name?.[0] || errorData.detail || 'Save failed');
			}

			addToast(isEditing ? 'Geometry updated!' : 'Geometry added!', 'success');

			// Après succès, rafraîchir et notifier
			if (!isEditing) resetForm();
			dispatch('geometryChanged');
			window.dispatchEvent(new Event('modelAdded'));
		} catch (error) {
			console.error('Submit error:', error);
			addToast(error.message, 'error');
		} finally {
			isLoading = false;
		}
	};

	const handleGeometrySelect = async (event: Event) => {
		const select = event.target as HTMLSelectElement;
		const id = select.value;
		if (id) {
			await loadGeometryDetails(id);
		} else {
			isEditing = false;
			resetForm();
		}
	};

	const deleteGeometry = async () => {
		if (!selectedGeometryId) return;
		try {
			const response = await fetch(`${API_ENDPOINTS.GEOMETRIES}${selectedGeometryId}/`, {
				method: 'DELETE'
			});
			if (!response.ok) throw new Error('Failed to delete geometry');
			addToast('Geometry deleted!', 'success');
			resetForm();
			dispatch('geometryChanged');
			window.dispatchEvent(new Event('modelAdded'));
		} catch (error) {
			console.error('Error deleting geometry:', error);
			addToast('Failed to delete geometry', 'error');
		}
	};

	const loadGeometryDetails = async (id: string) => {
		try {
			const response = await fetch(`${API_ENDPOINTS.GEOMETRIES}${id}/`);
			if (!response.ok) throw new Error('Failed to fetch geometry details');
			const geometry = await response.json();
			name = geometry.name;
			type = geometry.type;
			color = geometry.color;
			position = { ...geometry.position };
			rotation = { ...geometry.rotation };
			isEditing = true;
			selectedGeometryId = id;
			file = null; // On ne peut pas ré-éditer le fichier, donc on le vide
		} catch (error) {
			console.error('Error loading geometry details:', error);
			addToast('Failed to load geometry details', 'error');
		}
	};
</script>

<div class="form-container">
	<form
		onsubmit={(event) => {
			event.preventDefault();
			handleSubmit();
		}}
	>
		<h3>{isEditing ? 'Update' : 'Add'} Geometry</h3>

		<select bind:value={selectedGeometryId} onchange={handleGeometrySelect} class="geometry-select">
			<option value="">-- Add New Geometry --</option>
			{#each geometries as geometry}
				<option value={geometry.id}>{geometry.name}</option>
			{/each}
		</select>

		<input type="text" bind:value={name} placeholder="Name" required />

		{#if !file}
			<select bind:value={type}>
				{#each types as geometryType}
					<option value={geometryType}>{geometryType}</option>
				{/each}
			</select>
		{/if}

		<input type="color" bind:value={color} />

		<div class="position-rotation">
			<div>
				<label for="position-x">Position (X,Y,Z)</label>
				<input id="position-x" type="number" bind:value={position.x} placeholder="X" step="0.01" />
				<input id="position-y" type="number" bind:value={position.y} placeholder="Y" step="0.01" />
				<input id="position-z" type="number" bind:value={position.z} placeholder="Z" step="0.01" />
			</div>
			<div>
				<label for="rotation-x">Rotation (X,Y,Z)</label>
				<input id="rotation-x" type="number" bind:value={rotation.x} placeholder="X" step="0.01" />
				<input id="rotation-y" type="number" bind:value={rotation.y} placeholder="Y" step="0.01" />
				<input id="rotation-z" type="number" bind:value={rotation.z} placeholder="Z" step="0.01" />
			</div>
		</div>

		<div class="file-upload-section">
			<label for="file-upload">Or Upload a GLB/GLTF Model</label>
			<input
				id="file-upload"
				type="file"
				accept=".glb,.gltf"
				onchange={(e) => (file = e.target.files?.[0] || null)}
			/>
			{#if file}
				<p>Selected file: {file.name}</p>
			{/if}
		</div>

		<button type="submit" class={isEditing ? 'update-button' : 'add-button'} disabled={isLoading}>
			{isLoading ? 'Saving...' : isEditing ? 'Update' : 'Add'}
		</button>
		{#if isEditing}
			<button type="button" onclick={resetForm} class="cancel-button">Cancel</button>
		{/if}
	</form>

	<div class="delete-section">
		<button onclick={deleteGeometry} disabled={!selectedGeometryId} class="delete-button">
			Delete Selected
		</button>
	</div>
</div>

<style>
	.form-container {
		font-family: 'Inter', sans-serif;
		color: #fff;
		font-size: 0.85rem;
		width: 100%;
	}

	h3 {
		margin: 0 0 10px 0;
		font-size: 1rem;
		text-align: center;
		color: #4db6ac;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	input,
	select,
	button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		padding: 6px;
		border-radius: 4px;
		font-size: 0.8rem;
		width: 100%;
		box-sizing: border-box;
	}

	input:focus,
	select:focus {
		outline: none;
		border-color: #4db6ac;
	}

	.position-rotation {
		display: flex;
		gap: 5px;
	}

	.position-rotation > div {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	label {
		font-size: 0.7rem;
		color: #aaa;
		margin-bottom: 2px;
	}

	.add-button {
		background: #4db6ac;
		color: black;
		font-weight: bold;
		cursor: pointer;
		padding: 8px;
		margin-top: 5px;
	}

	.add-button:hover {
		background: #80cbc4;
	}

	.update-button {
		background: #ffb74d;
		color: black;
		font-weight: bold;
	}

	.cancel-button {
		background: transparent;
		border: 1px solid #777;
	}

	.delete-section {
		margin-top: 10px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		padding-top: 10px;
	}

	.delete-button {
		background: #ef5350;
		color: white;
		width: 100%;
	}
</style>
