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

	// Random Utils
	const getRandomValue = (min: number, max: number) => Number(Math.random() * (max - min) + min);
	const formatVal = (val: number) => Number(val.toFixed(2));

	// State for the form (runes)
	let name = $state('');
	let type = $state('box');
	let color = $state(
		`#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`
	);

	// Transforms
	let position = $state({ x: 0, y: 0, z: 0 });
	let rotation = $state({ x: 0, y: 0, z: 0 });
	let scale = $state({ x: 1, y: 1, z: 1 });
	let isUniformScale = $state(true);

	let file: File | null = $state(null); // State for the uploaded file

	interface GeometryItem {
		id: string;
		name: string;
		type: string;
		color: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		scale?: { x: number; y: number; z: number };
		visible: boolean;
	}

	let geometries = $state<GeometryItem[]>([]);
	let selectedGeometryId = $state('');
	let isEditing = $state(false);
	let types = $state<string[]>([]);
	let isDragging = $state(false);
	let fileInput = $state<HTMLInputElement>();
	let isLoading = $state(false);
	let isFormOpen = $state(false);
	let isDropdownOpen = $state(false);

	const toggleDropdown = () => {
		isDropdownOpen = !isDropdownOpen;
	};

	let isBloomActive = $state(true);
	let isTransformControlsEnabled = $state(false);
	let transformMode = $state<'translate' | 'rotate' | 'scale'>('translate');

	$effect(() => {
		window.dispatchEvent(
			new CustomEvent('toggleBloomEffect', {
				detail: { enabled: isBloomActive }
			})
		);
	});

	$effect(() => {
		window.dispatchEvent(
			new CustomEvent('toggleTransformControls', {
				detail: {
					enabled: isTransformControlsEnabled,
					id: selectedGeometryId,
					mode: transformMode
				}
			})
		);
	});

	const loadTypes = async () => {
		try {
			const response = await fetch(ENDPOINTS.TYPES, {
				headers: { Accept: 'application/json' }
			});
			if (!response.ok) throw new Error(`HTTP ${response.status}`);
			const data = await response.json();
			if (Array.isArray(data)) {
				const fetchedTypes = data.map((type) => type.id);
				// Ensure important types are present
				const baseTypes = [
					'box',
					'sphere',
					'torus',
					'icosahedron',
					'text',
					'spaceship',
					'vague',
					'nissangame',
					'bibigame'
				];
				types = [...new Set([...baseTypes, ...fetchedTypes])];
			}
		} catch (error) {
			console.error('Error loading types:', error);
			// Fallback types
			types = [
				'box',
				'sphere',
				'torus',
				'icosahedron',
				'text',
				'spaceship',
				'vague',
				'nissangame',
				'bibigame'
			];
			addToast('Failed to load types from server. Using defaults.', 'warning');
		}
	};

	const dispatch = createEventDispatcher();

	const resetForm = () => {
		// Default to 'box' or random type if available
		type = types.length > 0 ? types[Math.floor(Math.random() * types.length)] : 'box';
		name = type;

		// Random color
		color = `#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`;

		// Defaults: 0, 0, 0 for Pos/Rot, 1, 1, 1 for Scale
		position = { x: 0, y: 0, z: 0 };
		rotation = { x: 0, y: 0, z: 0 };
		scale = { x: 1, y: 1, z: 1 };
		isUniformScale = true;

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

		// Global listener for direct scene drops
		const handleDirectDrop = (e: any) => {
			if (e.detail?.file) {
				file = e.detail.file;
				if (!isEditing) name = file.name.split('.')[0];
				// Trigger immediate upload
				setTimeout(handleSubmit, 100);
			}
		};
		window.addEventListener('directSceneUpload', handleDirectDrop);

		// Synchronize UI when user manipulates in scene
		const handleManualSync = (e: any) => {
			if (e.detail?.id === selectedGeometryId) {
				const data = e.detail;
				if (data.position) position = { ...data.position };
				if (data.rotation) rotation = { ...data.rotation };
				if (data.scale) scale = { ...data.scale };

				// Optional: auto-save to DB after manual move
				if (e.detail.save) {
					handleSubmit();
				}
			}
		};
		window.addEventListener('manualTransformSync', handleManualSync);

		return () => {
			window.removeEventListener('directSceneUpload', handleDirectDrop);
			window.removeEventListener('manualTransformSync', handleManualSync);
		};
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

			const getUniqueName = (baseName: string) => {
				const existingNames = geometries.map((g) => g.name);
				if (!existingNames.includes(baseName)) return baseName;

				let counter = 1;
				while (existingNames.includes(`${baseName}-${counter}`)) {
					counter++;
				}
				return `${baseName}-${counter}`;
			};

			let uniqueName = isEditing ? name : '';

			if (!isEditing) {
				const baseName =
					name || (file ? file.name.split('.')[0] : type === 'text' ? 'Hello 3D' : type);
				uniqueName = getUniqueName(baseName);
			}

			formData.append('name', uniqueName);
			formData.append('color', color);
			formData.append('position', JSON.stringify(position));
			formData.append('rotation', JSON.stringify(rotation));
			formData.append('scale', JSON.stringify(scale));

			if (file) {
				formData.append('model_file', file);
				formData.append('type', 'gltf_model');
				const ext = file.name.split('.').pop()?.toLowerCase();
				if (ext) formData.append('model_type', ext);
			} else if (type === 'spaceship') {
				formData.append('type', 'gltf_model');
				formData.append('model_url', 'spaceship.glb'); // Backend helper or full URL
			} else {
				formData.append('type', type);
			}

			// For new items, force visible=true. For existing items, retain current visibility.
			if (!isEditing) {
				formData.append('visible', 'true');
			} else {
				// When editing, retrieve the current visibility state of the selected geometry
				const currentGeometry = geometries.find((g) => g.id === selectedGeometryId);
				if (currentGeometry) {
					formData.append('visible', String(currentGeometry.visible));
				}
			}

			let url = ENDPOINTS.GEOMETRIES;
			let method = 'POST';

			if (isEditing && selectedGeometryId) {
				url = `${url}${selectedGeometryId}/`;
				method = 'PUT';
			}

			const response = await fetch(url, {
				method,
				body: formData
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({ detail: 'Save failed' }));
				throw new Error(errorData.name?.[0] || errorData.detail);
			}

			addToast(isEditing ? 'Geometry updated!' : 'Geometry added!', 'success');

			// If adding new, select it? Or just reset?
			// User said "tu upload et vois direct".
			// If we re-load geometries, we should see it.

			if (!isEditing) resetForm();

			dispatch('geometryChanged');
			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries();
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
			await loadGeometries();
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
			position = geometry.position ? { ...geometry.position } : { x: 0, y: 0, z: 0 };
			rotation = geometry.rotation ? { ...geometry.rotation } : { x: 0, y: 0, z: 0 };
			scale = geometry.scale ? { ...geometry.scale } : { x: 1, y: 1, z: 1 };

			isEditing = true;
			selectedGeometryId = id;
			file = null;
		} catch (error) {
			console.error('Error loading geometry details:', error);
			addToast('Failed to load geometry details', 'error');
		}
	};

	const toggleGeometryVisibility = async (id: string) => {
		const originalGeometries = [...geometries];
		const geometry = geometries.find((g) => g.id === id);

		if (!geometry) return;

		const newVisibleState = !geometry.visible;

		// Optimistic update
		geometries = geometries.map((g) => (g.id === id ? { ...g, visible: newVisibleState } : g));
		window.dispatchEvent(
			new CustomEvent('geometryVisibilityChanged', {
				detail: { id, visible: newVisibleState }
			})
		);
		dispatch('geometryVisibilityChanged', { id, visible: newVisibleState });

		try {
			const response = await fetch(ENDPOINTS.TOGGLE_VISIBILITY(Number(id)), {
				method: 'PATCH'
			});

			if (!response.ok) {
				throw new Error('Failed to toggle visibility');
			}

			const data = await response.json();
			if (data.visible !== newVisibleState) {
				geometries = geometries.map((g) => (g.id === id ? { ...g, visible: data.visible } : g));
				window.dispatchEvent(
					new CustomEvent('geometryVisibilityChanged', {
						detail: { id, visible: data.visible }
					})
				);
			}

			window.dispatchEvent(new Event('modelAdded'));
			addToast(data.message, 'success');
		} catch (error) {
			console.error('Error toggling visibility:', error);
			geometries = originalGeometries;
			window.dispatchEvent(
				new CustomEvent('geometryVisibilityChanged', {
					detail: { id, visible: !newVisibleState }
				})
			);
			addToast(error instanceof Error ? error.message : 'Failed to toggle visibility', 'error');
		}
	};

	// Randomization Functions
	const randomizeVector = (
		current: { x: number; y: number; z: number },
		min: number,
		max: number
	) => {
		return {
			x: formatVal(getRandomValue(min, max)),
			y: formatVal(getRandomValue(min, max)),
			z: formatVal(getRandomValue(min, max))
		};
	};

	const randomizeVal = (min: number, max: number) => formatVal(getRandomValue(min, max));

	const randomizePosition = () => {
		position = randomizeVector(position, -5, 5);
	};
	const randomizeRotation = () => {
		rotation = randomizeVector(rotation, 0, 360);
	};
	const randomizeScale = () => {
		const s = randomizeVal(0.5, 3);
		scale = { x: s, y: s, z: s }; // Uniform random
	};

	const updateScale = (axis: 'x' | 'y' | 'z', val: number) => {
		scale[axis] = val;
		if (isUniformScale) {
			scale.x = val;
			scale.y = val;
			scale.z = val;
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
		<!-- Drag & Drop Upload Zone (Top of form) -->
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<div
			class="upload-container-wrapper"
			class:dragging={isDragging}
			ondragover={(e) => {
				e.preventDefault();
				isDragging = true;
			}}
			ondragleave={() => (isDragging = false)}
			ondrop={(e) => {
				e.preventDefault();
				isDragging = false;
				if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
					file = e.dataTransfer.files[0];
					if (!isEditing) name = file.name.split('.')[0];
				}
			}}
		>
			<div
				class="upload-zone-compact"
				class:has-file={!!file}
				role="button"
				tabindex="0"
				onclick={() => fileInput?.click()}
				title="Cliquez pour sélectionner un fichier"
			>
				<input
					bind:this={fileInput}
					type="file"
					accept=".glb,.gltf"
					style="display: none;"
					onchange={(e) => {
							const target = e.target as HTMLInputElement;
							if (target.files && target.files.length > 0) {
								file = target.files[0];
								if (!isEditing) name = file.name.split('.')[0];
							}
						}}
				/>

				{#if file}
					<div class="file-info-compact">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="18"
							height="18"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							class="file-icon"
							><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" /><polyline
								points="13 2 13 9 20 9"
							/></svg
						>
					</div>
				{:else}
					<div class="upload-placeholder-compact">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="20"
							height="20"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							class="upload-icon"
							><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline
								points="17 8 12 3 7 8"
							/><line x1="12" y1="3" x2="12" y2="15" /></svg
						>
					</div>
				{/if}
			</div>

			<div class="upload-label-zone">
				{#if file}
					<span class="filename-small">{file.name}</span>
				{:else}
					<span class="drop-hint">Glisser/Déposer fichier GLB ici</span>
				{/if}
			</div>
		</div>

		<h3>{isEditing ? 'Update' : 'Add'} Geometry</h3>

		<div class="geometry-list">
			<!-- Custom Dropdown Menu -->
			<div class="custom-dropdown">
				<!-- svelte-ignore a11y_click_events_have_key_events -->
				<div
					class="dropdown-header"
					onclick={toggleDropdown}
					role="button"
					tabindex="0"
					aria-label="Select a geometry to edit or add a new one"
				>
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

			<!-- Type Selection -->
			{#if !file}
				<div class="type-select-row">
					<select bind:value={type}>
						{#each types as geometryType}
							<option value={geometryType}>{geometryType}</option>
						{/each}
						<option value="text">text</option>
						<!-- Explicitly add text option -->
					</select>

					{#if type === 'text'}
						<input
							type="text"
							bind:value={name}
							placeholder="Enter text..."
							class="text-content-input"
						/>
					{:else}
						<input type="text" bind:value={name} placeholder="Name" required />
					{/if}
					<input type="color" bind:value={color} class="color-input" />
				</div>
			{:else}
				<input type="text" bind:value={name} placeholder="Name" required />
				<input type="color" bind:value={color} />
			{/if}

			<!-- Transform Controls: 3 Columns (Pos | Rot | Scl) -->
			<div class="transforms-grid">
				<!-- Header Row -->
				<div class="grid-header">
					<div class="col-header">
						<span>Pos</span>
						<button type="button" class="icon-btn tiny" onclick={randomizePosition} title="Rnd Pos"
							>🎲</button
						>
					</div>
					<div class="col-header">
						<span>Rot</span>
						<button type="button" class="icon-btn tiny" onclick={randomizeRotation} title="Rnd Rot"
							>🎲</button
						>
					</div>
					<div class="col-header">
						<span>Scl</span>
						<button type="button" class="icon-btn tiny" onclick={randomizeScale} title="Rnd Scl"
							>🎲</button
						>
						<button
							type="button"
							class="icon-btn tiny"
							class:active={isUniformScale}
							onclick={() => (isUniformScale = !isUniformScale)}
							title="Uniform">🔗</button
						>
					</div>
				</div>

				<!-- X Row -->
				<div class="grid-row">
					<div class="cell">
						<input
							type="number"
							bind:value={position.x}
							step="0.01"
							class="mini-input"
							placeholder="X"
						/>
					</div>
					<div class="cell">
						<input
							type="number"
							bind:value={rotation.x}
							step="0.01"
							class="mini-input"
							placeholder="X"
						/>
					</div>
					<div class="cell">
						<input
							type="number"
							bind:value={scale.x}
							step="0.01"
							class="mini-input"
							placeholder="X"
							oninput={(e) => updateScale('x', parseFloat(e.currentTarget.value) || 1)}
						/>
					</div>
				</div>

				<!-- Y Row -->
				<div class="grid-row">
					<div class="cell">
						<input
							type="number"
							bind:value={position.y}
							step="0.01"
							class="mini-input"
							placeholder="Y"
						/>
					</div>
					<div class="cell">
						<input
							type="number"
							bind:value={rotation.y}
							step="0.01"
							class="mini-input"
							placeholder="Y"
						/>
					</div>
					{#if isUniformScale}
						<div class="cell empty" />
					{:else}
						<div class="cell">
							<input
								type="number"
								bind:value={scale.y}
								step="0.01"
								class="mini-input"
								placeholder="Y"
							/>
						</div>
					{/if}
				</div>

				<!-- Z Row -->
				<div class="grid-row">
					<div class="cell">
						<input
							type="number"
							bind:value={position.z}
							step="0.01"
							class="mini-input"
							placeholder="Z"
						/>
					</div>
					<div class="cell">
						<input
							type="number"
							bind:value={rotation.z}
							step="0.01"
							class="mini-input"
							placeholder="Z"
						/>
					</div>
					{#if isUniformScale}
						<div class="cell">
							<input
								type="number"
								value={scale.z}
								step="0.01"
								class="mini-input readonly"
								placeholder="Z"
								readonly
							/>
						</div>
					{:else}
						<div class="cell">
							<input
								type="number"
								bind:value={scale.z}
								step="0.01"
								class="mini-input"
								placeholder="Z"
							/>
						</div>
					{/if}
				</div>
			</div>

			<button type="submit" class={isEditing ? 'update-button' : 'add-button'} disabled={isLoading}>
				{isLoading ? 'Saving...' : isEditing ? 'Update' : 'Add'}
			</button>
			{#if isEditing}
				<button type="button" onclick={resetForm} class="cancel-button">Cancel</button>
			{/if}
		</div>

		<!-- Scene Controls -->
		<div class="scene-controls">
			<div class="control-item">
				<span>Bloom Effect</span>
				<button
					type="button"
					class="toggle-btn"
					class:active={isBloomActive}
					onclick={() => (isBloomActive = !isBloomActive)}
				>
					{isBloomActive ? 'Enabled' : 'Disabled'}
				</button>
			</div>

			<div class="control-item transform-controls-row">
				<span>Manipuler (Direct)</span>
				<div class="transform-actions-v2">
					<button
						type="button"
						class="mode-btn toggle"
						class:active={isTransformControlsEnabled}
						onclick={() => (isTransformControlsEnabled = !isTransformControlsEnabled)}
						title="Activer Gizmo"
					>
						{isTransformControlsEnabled ? 'ON' : 'OFF'}
					</button>

					<div class="mode-selector-group" class:disabled={!isTransformControlsEnabled}>
						<button
							type="button"
							class="mode-btn"
							class:active={transformMode === 'translate'}
							onclick={() => (transformMode = 'translate')}>Pos</button
						>
						<button
							type="button"
							class="mode-btn"
							class:active={transformMode === 'rotate'}
							onclick={() => (transformMode = 'rotate')}>Rot</button
						>
						<button
							type="button"
							class="mode-btn"
							class:active={transformMode === 'scale'}
							onclick={() => (transformMode = 'scale')}>Scl</button
						>
					</div>
				</div>
			</div>
		</div>
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
		font-size: 0.75rem;
		width: 100%;
		margin: 0;
		background: rgba(255, 255, 255, 0.03);
		padding: 8px;
		border-radius: 6px;
		border: 1px solid rgba(255, 255, 255, 0.08);
		box-sizing: border-box;
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

	/* Type Select Row */
	.type-select-row {
		display: flex;
		gap: 6px;
		align-items: center;
	}
	.type-select-row select {
		flex: 1;
	}
	.text-content-input,
	.color-input {
		flex: 1;
	}
	.color-input {
		max-width: 40px;
		padding: 0;
		border: 0;
		height: 24px;
	}

	/* Transforms Grid */
	.transforms-grid {
		display: flex;
		flex-direction: column;
		gap: 2px;
		margin-top: 5px;
		background: rgba(0, 0, 0, 0.2);
		padding: 4px;
		border-radius: 4px;
	}

	.grid-header {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 4px;
		margin-bottom: 2px;
	}

	.col-header {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
		font-size: 0.65rem;
		font-weight: bold;
		color: #bbb;
		text-transform: uppercase;
	}

	.grid-row {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 4px;
	}

	.cell {
		display: flex;
		align-items: center;
	}

	.cell.empty {
		visibility: hidden;
	}

	.mini-input {
		width: 100%;
		padding: 2px 4px;
		font-size: 0.7rem;
		text-align: center;
		background: rgba(255, 255, 255, 0.07);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: #ddd;
		border-radius: 2px;
	}

	.mini-input:focus {
		border-color: #4db6ac;
		background: rgba(255, 255, 255, 0.1);
	}

	.mini-input.readonly {
		opacity: 0.6;
		cursor: not-allowed;
		background: rgba(0, 0, 0, 0.2);
	}

	.icon-btn.tiny {
		padding: 0 2px;
		font-size: 0.7rem;
		background: transparent;
		border: none;
		color: #777;
		cursor: pointer;
	}

	.icon-btn.tiny:hover {
		color: #4db6ac;
	}

	.icon-btn.active {
		color: #4db6ac;
	}

	.reset-button {
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

	/* Scene Controls */
	.scene-controls {
		margin-top: 10px;
		padding-top: 8px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
	}

	.control-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.7rem;
		color: #bbb;
	}

	.toggle-btn {
		width: auto;
		padding: 2px 8px;
		font-size: 0.65rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		transition: all 0.2s;
	}

	/* Compact Upload Zone */
	.upload-container-wrapper {
		display: flex;
		align-items: center;
		gap: 12px;
		background: rgba(0, 0, 0, 0.2);
		border: 1px dashed rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 6px 12px;
		margin-bottom: 10px;
		transition: all 0.2s ease;
	}
	.upload-container-wrapper.dragging {
		border-color: #4db6ac;
		background: rgba(77, 182, 172, 0.1);
	}
	.upload-zone-compact {
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 6px;
		cursor: pointer;
		color: #4db6ac;
		transition: transform 0.1s;
	}
	.upload-zone-compact:hover {
		background: rgba(255, 255, 255, 0.1);
		transform: scale(1.05);
	}
	.upload-zone-compact.has-file {
		color: #4caf50;
		border-color: #4caf50;
	}
	.upload-label-zone {
		flex: 1;
		font-size: 0.7rem;
		color: #888;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.filename-small {
		color: #80cbc4;
		font-weight: 500;
	}
	.drop-hint {
		font-style: italic;
	}

	.transform-actions-v2 {
		display: flex;
		gap: 8px;
		align-items: center;
	}

	.mode-selector-group {
		display: flex;
		background: rgba(0, 0, 0, 0.2);
		border-radius: 4px;
		padding: 2px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		transition: opacity 0.2s;
	}

	.mode-selector-group.disabled {
		opacity: 0.3;
		pointer-events: none;
	}

	.mode-btn {
		background: transparent;
		border: none;
		color: #777;
		padding: 2px 6px;
		font-size: 0.65rem;
		cursor: pointer;
		border-radius: 2px;
		transition: all 0.2s;
	}

	.mode-btn:hover {
		color: #eee;
	}

	.mode-btn.active {
		background: rgba(77, 182, 172, 0.2);
		color: #4db6ac;
	}

	.mode-btn.toggle {
		border: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.05);
		padding: 3px 8px;
		border-radius: 12px;
	}

	.mode-btn.toggle.active {
		background: rgba(77, 182, 172, 0.2);
		border-color: #4db6ac;
	}

	.toggle-btn.active {
		background: rgba(77, 182, 172, 0.2);
		color: #4db6ac;
		border-color: #4db6ac;
	}
</style>
