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

	interface GeometryItem {
		id: string;
		name: string;
		type: string;
		color: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		visible: boolean; // Add visible property
		// Add other properties as needed
	}

	let geometries = $state<GeometryItem[]>([]);
	let selectedGeometryId = $state('');
	let isEditing = $state(false);
	let types = $state<string[]>([]);
	let isLoading = $state(false);
	let isFormOpen = $state(false);
	let isDropdownOpen = $state(false);

	const toggleDropdown = () => {
		isDropdownOpen = !isDropdownOpen;
	};

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

	const toggleGeometryVisibility = async (id: string) => {
		// Optimistic update: toggle locally first
		const originalGeometries = [...geometries];
		const geometry = geometries.find((g) => g.id === id);

		if (!geometry) return;

		const newVisibleState = !geometry.visible;

		// Update UI immediately
		geometries = geometries.map((g) => (g.id === id ? { ...g, visible: newVisibleState } : g));
		// Dispatch event for other components (Scene)
		window.dispatchEvent(
			new CustomEvent('geometryVisibilityChanged', {
				detail: { id, visible: newVisibleState }
			})
		);
		// Also dispatch Svelte event
		dispatch('geometryVisibilityChanged', { id, visible: newVisibleState });

		// Call backend to persist
		try {
			const response = await fetch(ENDPOINTS.TOGGLE_VISIBILITY(Number(id)), {
				method: 'PATCH'
			});

			if (!response.ok) {
				throw new Error('Failed to toggle visibility');
			}

			const data = await response.json();
			// Optional: verify backend state matches local state
			if (data.visible !== newVisibleState) {
				// Correction if backend logic differs (unlikely)
				geometries = geometries.map((g) => (g.id === id ? { ...g, visible: data.visible } : g));
				window.dispatchEvent(
					new CustomEvent('geometryVisibilityChanged', {
						detail: { id, visible: data.visible }
					})
				);
			}

			// Trigger other components to refresh if needed (like the scene)
			window.dispatchEvent(new Event('modelAdded'));

			addToast(data.message, 'success');
		} catch (error) {
			console.error('Error toggling visibility:', error);
			// Revert on error
			geometries = originalGeometries;
			window.dispatchEvent(
				new CustomEvent('geometryVisibilityChanged', {
					detail: { id, visible: !newVisibleState }
				})
			);
			addToast(error instanceof Error ? error.message : 'Failed to toggle visibility', 'error');
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
				<!-- Custom Dropdown Menu -->
				<div class="custom-dropdown">
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<div class="dropdown-header" onclick={toggleDropdown} role="button" tabindex="0">
						<span>
							{selectedGeometryId
								? geometries.find((g) => g.id === selectedGeometryId)?.name || 'Unknown Geometry'
								: '-- Select Geometry --'}
						</span>
						<svg
							class="chevron"
							class:open={isDropdownOpen}
							xmlns="http://www.w3.org/2000/svg"
							width="16"
							height="16"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"><polyline points="6 9 12 15 18 9" /></svg
						>
					</div>

					{#if isDropdownOpen}
						<div class="dropdown-list">
							{#each geometries as geometry (geometry.id)}
								<div class="dropdown-item" class:selected={selectedGeometryId === geometry.id}>
									<!-- Name: Selects and closes form (Re-enroule le ruban) -->
									<div
										class="item-name"
										onclick={() => {
											loadGeometryDetails(geometry.id);
											isFormOpen = false; // Close form
											isDropdownOpen = false; // Close dropdown
										}}
										role="button"
										tabindex="0"
										onkeydown={(e) => {
											if (e.key === 'Enter' || e.key === ' ') {
												loadGeometryDetails(geometry.id);
												isFormOpen = false;
												isDropdownOpen = false;
											}
										}}
									>
										{geometry.name}
									</div>

									<!-- Eye: Toggles Visibility (stays open or just updates state) -->
									<button
										type="button"
										class="visibility-toggle"
										class:visible={geometry.visible}
										class:hidden={!geometry.visible}
										onclick={(e) => {
											e.stopPropagation();
											toggleGeometryVisibility(geometry.id);
										}}
										aria-label={geometry.visible ? 'Hide' : 'Show'}
									>
										{#if geometry.visible}
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="14"
												height="14"
												viewBox="0 0 24 24"
												fill="none"
												stroke="currentColor"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle
													cx="12"
													cy="12"
													r="3"
												/></svg
											>
										{:else}
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="14"
												height="14"
												viewBox="0 0 24 24"
												fill="none"
												stroke="currentColor"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												><path
													d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
												/><line x1="1" y1="1" x2="23" y2="23" /></svg
											>
										{/if}
									</button>
								</div>
							{/each}

							{#if geometries.length === 0}
								<div class="dropdown-item empty">No geometries found</div>
							{/if}
						</div>
					{/if}
				</div>

				<button
					type="button"
					class="add-new-button"
					onclick={() => {
						resetForm();
						isEditing = false;
					}}
				>
					+ Add New Geometry
				</button>

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

				<button
					type="submit"
					class={isEditing ? 'update-button' : 'add-button'}
					disabled={isLoading}
				>
					{isLoading ? 'Saving...' : isEditing ? 'Update' : 'Add'}
				</button>
				{#if isEditing}
					<button type="button" onclick={resetForm} class="cancel-button">Cancel</button>
				{/if}
			</div>
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

	/* Custom Dropdown Styles */
	.custom-dropdown {
		position: relative;
		margin-bottom: 10px;
		width: 100%;
		font-family: 'Inter', sans-serif;
	}

	.dropdown-header {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgb(160, 155, 155);
		padding: 6px 10px;
		border-radius: 3px;
		cursor: pointer;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.75rem;
		transition: border-color 0.2s;
	}

	.dropdown-header:hover {
		border-color: #4db6ac;
	}

	.chevron {
		transition: transform 0.2s ease;
		color: #999;
	}

	.chevron.open {
		transform: rotate(180deg);
	}

	.dropdown-list {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: #1a1a1a;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		margin-top: 4px;
		max-height: 200px;
		overflow-y: auto;
		z-index: 1000;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
	}

	.dropdown-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 8px 10px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		transition: background 0.1s;
	}

	.dropdown-item:last-child {
		border-bottom: none;
	}

	.dropdown-item:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.dropdown-item.selected {
		background: rgba(77, 182, 172, 0.15);
		color: #80cbc4;
	}

	.item-name {
		flex: 1;
		font-size: 0.75rem;
		color: #ddd;
		cursor: pointer;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.dropdown-item.selected .item-name {
		color: #80cbc4;
		font-weight: 500;
	}

	.dropdown-item.empty {
		padding: 10px;
		text-align: center;
		color: #777;
		font-style: italic;
	}

	/* Reusing visibility-toggle style from existing code, ensuring it fits */
	.visibility-toggle {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: #fff;
		padding: 4px;
		border-radius: 3px;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		margin-left: 8px;
	}

	.visibility-toggle:hover {
		transform: scale(1.1);
		border-color: #fff;
	}

	.visibility-toggle.visible {
		color: #4caf50;
		border-color: rgba(76, 175, 80, 0.5);
		background: rgba(76, 175, 80, 0.1);
	}

	.visibility-toggle.hidden {
		color: #f44336;
		border-color: rgba(244, 67, 54, 0.5);
		background: rgba(244, 67, 54, 0.1);
	}
</style>
