<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { addToast } from '$lib/stores/toasts';
	import { ENDPOINTS } from '$lib/config';

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

	let geometries = $state<any[]>([]);
	let selectedGeometryId = $state('');
	let isEditing = $state(false);
	let types = $state<string[]>([]);
	let isLoading = $state(false);
	let isFormOpen = $state(false);

	const loadTypes = async () => {
		try {
			const response = await fetch(ENDPOINTS.TYPES, {
				headers: { Accept: 'application/json' }
			});
			if (!response.ok) throw new Error(`HTTP ${response.status}`);
			const data = await response.json();
			if (Array.isArray(data)) {
				types = data.map((type) => type.id);
			}
		} catch (error) {
			console.error('Error loading types:', error);
			addToast('Failed to load types.', 'error');
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
			const response = await fetch(ENDPOINTS.GEOMETRIES, {
				headers: { Accept: 'application/json' }
			});
			if (!response.ok) throw new Error(`HTTP ${response.status}`);
			const data = await response.json();
			if (data.results && Array.isArray(data.results)) {
				geometries = data.results;
			} else if (Array.isArray(data)) {
				geometries = data;
			}
		} catch (error) {
			console.error('Error loading geometries:', error);
			addToast('Failed to load geometries.', 'error');
		}
	};

	const handleSubmit = async () => {
		isLoading = true;
		try {
			const formData = new FormData();

			const randomId = Math.random().toString(36).substring(2, 7);
			const uniqueName = isEditing
				? name
				: `${name || (file ? file.name.split('.')[0] : 'geo')}-${randomId}`;

			formData.append('name', uniqueName);
			formData.append('color', color);
			formData.append('position', JSON.stringify(position));
			formData.append('rotation', JSON.stringify(rotation));

			if (file) {
				formData.append('model_file', file);
				formData.append('type', 'gltf_model');
				const ext = file.name.split('.').pop()?.toLowerCase();
				if (ext) formData.append('model_type', ext);
			} else {
				formData.append('type', type);
			}

			let url = ENDPOINTS.GEOMETRIES;
			let method = 'POST';

			if (isEditing && selectedGeometryId) {
				url = `${url}${selectedGeometryId}/`;
				method = 'PUT'; // PUT pour une mise à jour complète
			}

			const response = await fetch(url, {
				method,
				body: formData
				// Pas de 'Content-Type', le navigateur le définit correctement pour FormData
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({ detail: 'Save failed' }));
				throw new Error(errorData.name?.[0] || errorData.detail);
			}

			addToast(isEditing ? 'Geometry updated!' : 'Geometry added!', 'success');

			if (!isEditing) resetForm();
			dispatch('geometryChanged');
			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries(); // Recharger la liste
		} catch (error) {
			console.error('Submit error:', error);
			addToast(error instanceof Error ? error.message : 'Save failed', 'error');
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
			const response = await fetch(`${ENDPOINTS.GEOMETRIES}${selectedGeometryId}/`, {
				method: 'DELETE'
			});
			if (!response.ok) throw new Error('Failed to delete geometry');
			addToast('Geometry deleted!', 'success');
			resetForm();
			dispatch('geometryChanged');
			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries(); // Recharger la liste
		} catch (error) {
			console.error('Error deleting geometry:', error);
			addToast('Failed to delete geometry', 'error');
		}
	};

	const toggleVisibility = async (id: number) => {
		try {
			const response = await fetch(ENDPOINTS.TOGGLE_VISIBILITY(id), {
				method: 'PATCH'
			});
			if (!response.ok) throw new Error('Failed to toggle visibility');
			const data = await response.json();
			addToast(data.message, 'success');
			await loadGeometries(); // Recharger la liste
		} catch (error) {
			console.error('Error toggling visibility:', error);
			addToast(error instanceof Error ? error.message : 'Failed to toggle visibility', 'error');
		}
	};

	const loadGeometryDetails = async (id: string) => {
		try {
			const response = await fetch(`${ENDPOINTS.GEOMETRIES}${id}/`);
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

<div
	class="form-wrapper"
	class:is-open={isFormOpen}
	onmouseenter={() => (isFormOpen = true)}
	onmouseleave={() => (isFormOpen = false)}
>
	<div class="form-container">
		<form
			onsubmit={(event) => {
				event.preventDefault();
				handleSubmit();
			}}
		>
			<h3>{isEditing ? 'Update' : 'Add'} Geometry</h3>

			<div class="geometry-list">
				<select
					bind:value={selectedGeometryId}
					onchange={handleGeometrySelect}
					class="geometry-select"
				>
					<option value="">-- Add New Geometry --</option>
					{#each geometries as geometry}
						<option value={geometry.id}>
							{geometry.name}
							{geometry.visible ? '👁️' : '🚫'}
						</option>
					{/each}
				</select>

				<div class="geometry-actions">
					{#each geometries as geometry}
						<div class="geometry-item" class:selected={geometry.id === selectedGeometryId}>
							<span class="geometry-name">{geometry.name}</span>
							<div class="geometry-controls">
								<button
									class="visibility-toggle"
									class:visible={geometry.visible}
									class:hidden={!geometry.visible}
									onclick={() => toggleVisibility(geometry.id)}
									title={geometry.visible ? 'Hide geometry' : 'Show geometry'}
								>
									{geometry.visible ? '👁️' : '🚫'}
								</button>
								<button
									class="select-geometry"
									onclick={() => {
										selectedGeometryId = geometry.id;
										loadGeometryDetails(geometry.id);
									}}
									title="Select geometry for editing"
								>
									✏️
								</button>
							</div>
						</div>
					{/each}
				</div>
			</div>

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
					<input
						id="position-x"
						type="number"
						bind:value={position.x}
						placeholder="X"
						step="0.01"
					/>
					<input
						id="position-y"
						type="number"
						bind:value={position.y}
						placeholder="Y"
						step="0.01"
					/>
					<input
						id="position-z"
						type="number"
						bind:value={position.z}
						placeholder="Z"
						step="0.01"
					/>
					<button
						type="button"
						onclick={() => (position = { x: 0, y: 0, z: 0 })}
						class="reset-button"
					>
						Reset Position
					</button>
				</div>
				<div>
					<label for="rotation-x">Rotation (X,Y,Z)</label>
					<input
						id="rotation-x"
						type="number"
						bind:value={rotation.x}
						placeholder="X"
						step="0.01"
					/>
					<input
						id="rotation-y"
						type="number"
						bind:value={rotation.y}
						placeholder="Y"
						step="0.01"
					/>
					<input
						id="rotation-z"
						type="number"
						bind:value={rotation.z}
						placeholder="Z"
						step="0.01"
					/>
					<button
						type="button"
						onclick={() => (rotation = { x: 0, y: 0, z: 0 })}
						class="reset-button"
					>
						Reset Rotation
					</button>
				</div>
			</div>

			<div class="file-upload-section">
				<label for="file-upload">Or Upload a GLB/GLTF Model</label>
				<input
					id="file-upload"
					type="file"
					accept=".glb,.gltf"
					onchange={(e) => {
						const target = e.target as HTMLInputElement;
						file = target.files?.[0] || null;
					}}
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
</div>

<!-- Closing div for form-wrapper -->

<style>
	.form-container {
		font-family: 'Inter', sans-serif;
		color: #fff;
		font-size: 0.75rem;
		width: 100%;
		background: rgba(255, 255, 255, 0.03);
		padding: 12px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.05);
	}

	h3 {
		margin: 0 0 12px 0;
		font-size: 0.85rem;
		text-align: center;
		color: #4db6ac;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	input,
	select,
	button {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgb(160, 155, 155);
		padding: 4px 6px;
		border-radius: 3px;
		font-size: 0.7rem;
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
		font-size: 0.6rem;
		color: #999;
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

	.reset-button {
		background: linear-gradient(135deg, #4db6ac, #80cbc4);
		border: 1px solid #4db6ac;
		color: black;
		font-size: 0.7rem;
		font-weight: 600;
		padding: 6px 10px;
		margin-top: 8px;
		cursor: pointer;
		align-self: flex-end;
		width: auto;
		border-radius: 4px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: all 0.2s ease;
	}

	.reset-button:hover {
		background: linear-gradient(135deg, #80cbc4, #4db6ac);
		border-color: #80cbc4;
		transform: translateY(-1px);
		box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
	}

	.geometry-list {
		margin-bottom: 10px;
	}

	.geometry-actions {
		max-height: 200px;
		overflow-y: auto;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		margin-top: 5px;
	}

	.geometry-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 6px 8px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		transition: background-color 0.2s ease;
	}

	.geometry-item:last-child {
		border-bottom: none;
	}

	.geometry-item.selected {
		background: rgba(77, 182, 172, 0.2);
	}

	.geometry-name {
		font-size: 0.7rem;
		color: #ccc;
		flex: 1;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.geometry-controls {
		display: flex;
		gap: 4px;
	}

	.visibility-toggle,
	.select-geometry {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: #fff;
		padding: 2px 6px;
		border-radius: 3px;
		font-size: 0.8rem;
		cursor: pointer;
		transition: all 0.2s ease;
		min-width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.visibility-toggle.visible {
		background: rgba(76, 175, 80, 0.3);
		border-color: #4caf50;
	}

	.visibility-toggle.hidden {
		background: rgba(244, 67, 54, 0.3);
		border-color: #f44336;
	}

	.visibility-toggle:hover {
		transform: scale(1.1);
	}

	.select-geometry:hover {
		background: rgba(255, 152, 0, 0.3);
		border-color: #ff9800;
		transform: scale(1.1);
	}
</style>
