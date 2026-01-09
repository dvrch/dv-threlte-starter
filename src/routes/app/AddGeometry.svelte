<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { addToast } from '$lib/stores/toasts';
	import { ENDPOINTS } from '$lib/config';
	import { base } from '$app/paths';
	import { geometryService, type GeometryItem } from '$lib/services/api';

	const { selectedGeometry = null } = $props();

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
	let position = $state({ x: 0, y: 0, z: 0 });
	let rotation = $state({ x: 0, y: 0, z: 0 });
	let scale = $state({ x: 1, y: 1, z: 1 });
	let isUniformScale = $state(true);
	let file: File | null = $state(null);

	let geometries = $state<GeometryItem[]>([]);
	let selectedGeometryId = $state('');
	let isEditing = $state(false);
	let types = $state<string[]>([]);
	let isDragging = $state(false);
	let fileInput = $state<HTMLInputElement>();
	let isLoading = $state(false);
	let isDropdownOpen = $state(false);

	let isBloomActive = $state(true);
	let isPremiumActive = $state(true);
	let isTransformControlsEnabled = $state(false);
	let transformModes = $state<('translate' | 'rotate' | 'scale')[]>(['translate']);
	let searchQuery = $state('');

	let filteredGeometries = $derived(
		geometries.filter((g) => g.name.toLowerCase().includes(searchQuery.toLowerCase()))
	);

	$effect(() => {
		if (selectedGeometry && selectedGeometry.id !== selectedGeometryId) {
			loadGeometryDetails(selectedGeometry.id);
		}
	});

	$effect(() => {
		window.dispatchEvent(
			new CustomEvent('toggleBloomEffect', { detail: { enabled: isBloomActive } })
		);
	});

	$effect(() => {
		window.dispatchEvent(
			new CustomEvent('toggleTransformControls', {
				detail: {
					enabled: isTransformControlsEnabled,
					id: selectedGeometryId,
					modes: transformModes
				}
			})
		);
	});

	$effect(() => {
		window.dispatchEvent(
			new CustomEvent('togglePremiumEffect', { detail: { enabled: isPremiumActive } })
		);
	});

	const loadTypes = async () => {
		try {
			const staticResponse = await fetch(`${base}/data/types.json`);
			if (staticResponse.ok) {
				const data = await staticResponse.json();
				const fetchedTypes = (data || []).map((t: any) => t.id);
				const systemTypes = ['box', 'sphere', 'torus', 'icosahedron', 'textmd', 'image_plane'];
				types = [...new Set([...systemTypes, ...fetchedTypes])];
			}
		} catch (error) {
			types = ['box', 'sphere', 'torus', 'icosahedron', 'textmd', 'image_plane'];
		}
	};

	const dispatch = createEventDispatcher();

	const resetForm = () => {
		type = types.length > 0 ? 'box' : 'box';
		name = '';
		color = `#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`;
		position = { x: 0, y: 0, z: 0 };
		rotation = { x: 0, y: 0, z: 0 };
		scale = { x: 1, y: 1, z: 1 };
		isUniformScale = true;
		isEditing = false;
		selectedGeometryId = '';
		file = null;
	};

	const loadGeometries = async () => {
		try {
			geometries = await geometryService.getAll();
		} catch (error) {
			addToast('Failed to load geometries.', 'error');
		}
	};

	const handleSubmit = async () => {
		isLoading = true;
		try {
			const formData = new FormData();
			const baseName = name || (file ? file.name.split('.')[0] : type);
			formData.append('name', baseName);
			formData.append('color', color);
			formData.append('position', JSON.stringify(position));
			formData.append('rotation', JSON.stringify(rotation));
			formData.append('scale', JSON.stringify(scale));

			if (file) {
				formData.append('model_file', file);
				const ext = file.name.split('.').pop()?.toLowerCase() || '';
				const isImage = ['jpg', 'jpeg', 'png', 'webp'].includes(ext);
				formData.append('type', isImage ? 'image_plane' : 'gltf_model');
			} else {
				formData.append('type', type === 'text' ? 'text' : type);
			}

			if (!isEditing) formData.append('visible', 'true');
			else {
				const current = geometries.find((g) => g.id === selectedGeometryId);
				if (current) formData.append('visible', String(current.visible));
			}

			await geometryService.save(formData, isEditing ? selectedGeometryId : undefined);
			addToast(isEditing ? 'Mis à jour !' : 'Ajouté !', 'success');
			if (!isEditing) resetForm();

			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries();
		} catch (error) {
			addToast('Erreur de sauvegarde', 'error');
		} finally {
			isLoading = false;
		}
	};

	const loadGeometryDetails = async (id: string) => {
		const g = geometries.find((g) => g.id == id);
		if (!g) return;
		name = g.name;
		type = g.type;
		color = g.color;
		position = { ...g.position };
		rotation = { ...g.rotation };
		scale = { ...g.scale };
		isEditing = true;
		selectedGeometryId = id;
		file = null;
	};

	const toggleGeometryVisibility = async (id: string) => {
		const g = geometries.find((g) => g.id === id);
		if (!g) return;
		const next = !g.visible;
		geometries = geometries.map((i) => (i.id === id ? { ...i, visible: next } : i));
		window.dispatchEvent(
			new CustomEvent('geometryVisibilityChanged', { detail: { id, visible: next } })
		);
		const fd = new FormData();
		fd.append('visible', String(next));
		await geometryService.save(fd, id);
	};

	const handleExport = () => geometryService.exportScene();
	const handleExportSQLite = () => geometryService.exportSceneToSQLite();

	onMount(() => {
		loadTypes();
		loadGeometries();

		const handleDirectDrop = (e: any) => {
			if (e.detail?.file) {
				file = e.detail.file;
				name = file?.name.split('.')[0] || '';
				setTimeout(handleSubmit, 100);
			}
		};

		const handleDirectImport = async (e: any) => {
			await geometryService.importScene(e.detail.file);
			await loadGeometries();
			window.dispatchEvent(new Event('modelAdded'));
			addToast('Scène importée !', 'success');
		};

		const handleManualSync = (e: any) => {
			const data = e.detail;
			if (!data?.id) return;
			if (data.id !== selectedGeometryId) {
				loadGeometryDetails(data.id);
				return;
			}
			if (data.position)
				position = {
					x: formatVal(data.position.x),
					y: formatVal(data.position.y),
					z: formatVal(data.position.z)
				};
			if (data.rotation)
				rotation = {
					x: formatVal(data.rotation.x),
					y: formatVal(data.rotation.y),
					z: formatVal(data.rotation.z)
				};
			if (data.scale)
				scale = {
					x: formatVal(data.scale.x),
					y: formatVal(data.scale.y),
					z: formatVal(data.scale.z)
				};
			if (data.save) handleSubmit();
		};

		window.addEventListener('directSceneUpload', handleDirectDrop);
		window.addEventListener('directSceneImport', handleDirectImport);
		window.addEventListener('manualTransformSync', handleManualSync);
		return () => {
			window.removeEventListener('directSceneUpload', handleDirectDrop);
			window.removeEventListener('directSceneImport', handleDirectImport);
			window.removeEventListener('manualTransformSync', handleManualSync);
		};
	});
</script>

<div class="form-container">
	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleSubmit();
		}}
	>
		<div class="upload-container-wrapper" class:dragging={isDragging}>
			<div class="upload-controls-grid">
				<div
					class="upload-zone-compact"
					class:has-file={!!file}
					onclick={() => fileInput?.click()}
					role="button"
					tabindex="0"
				>
					<input
						bind:this={fileInput}
						type="file"
						accept=".glb,.gltf"
						style="display: none;"
						onchange={(e) => { 
						const t = e.target as HTMLInputElement; 
						if (t.files?.[0]) { file = t.files[0]; name = file.name.split('.')[0]; } 
					}}
					/>
					{file ? '✅' : '📤'}
				</div>

				<div class="mini-controls-table">
					<div class="mini-control-cell top-right">
						<div class="hand-icon" class:active={isEditing}>✍️</div>
					</div>
					<div class="mini-control-cell bottom-left">
						<button
							type="button"
							class="tiny-btn"
							class:active={transformModes.includes('translate')}
							onclick={() => (transformModes = ['translate'])}>P</button
						>
						<button
							type="button"
							class="tiny-btn"
							class:active={transformModes.includes('rotate')}
							onclick={() => (transformModes = ['rotate'])}>R</button
						>
						<button
							type="button"
							class="tiny-btn"
							class:active={transformModes.includes('scale')}
							onclick={() => (transformModes = ['scale'])}>S</button
						>
					</div>
					<div class="mini-control-cell bottom-right">
						<button
							type="button"
							class="tiny-toggle"
							class:active={isTransformControlsEnabled}
							onclick={() => (isTransformControlsEnabled = !isTransformControlsEnabled)}>✜</button
						>
					</div>
				</div>
			</div>
		</div>

		<div class="geometry-list">
			<div class="custom-dropdown" onmouseleave={() => (isDropdownOpen = false)} role="region">
				<div
					class="dropdown-header"
					onclick={() => (isDropdownOpen = !isDropdownOpen)}
					onmouseenter={() => (isDropdownOpen = true)}
					role="button"
					tabindex="0"
				>
					<span
						>{selectedGeometryId
							? geometries.find((g) => g.id === selectedGeometryId)?.name
							: '-- Select --'}</span
					>
				</div>
				{#if isDropdownOpen}
					<div class="dropdown-list">
						<div class="dropdown-search">
							<input
								type="text"
								bind:value={searchQuery}
								placeholder="Filter..."
								onclick={(e) => e.stopPropagation()}
							/>
						</div>
						{#each filteredGeometries as g (g.id)}
							<div class="dropdown-item" class:selected={selectedGeometryId === g.id}>
								<div
									class="item-name"
									onclick={() => {
										loadGeometryDetails(g.id);
										isDropdownOpen = false;
									}}
									role="button"
									tabindex="0"
								>
									{g.name}
								</div>
								<button
									type="button"
									class="visibility-toggle"
									class:visible={g.visible}
									onclick={() => toggleGeometryVisibility(g.id)}>{g.visible ? '👁️' : '🕶️'}</button
								>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<div class="type-select-row">
				<select bind:value={type}>
					{#each types as t}<option value={t}>{t}</option>{/each}
					<option value="text">text</option>
				</select>
				<input type="text" bind:value={name} placeholder="Name" required />
				<input type="color" bind:value={color} class="color-input" />
			</div>
		</div>

		<div class="transform-grid mini">
			<div class="vector-input-row">
				<label>POS</label>
				<input type="number" bind:value={position.x} step="0.1" />
				<input type="number" bind:value={position.y} step="0.1" />
				<input type="number" bind:value={position.z} step="0.1" />
			</div>
			<div class="vector-input-row">
				<label>ROT</label>
				<input type="number" bind:value={rotation.x} step="1" />
				<input type="number" bind:value={rotation.y} step="1" />
				<input type="number" bind:value={rotation.z} step="1" />
			</div>
			<div class="vector-input-row">
				<label>SCL</label>
				<input
					type="number"
					bind:value={scale.x}
					step="0.1"
					oninput={(e) => isUniformScale && (scale.y = scale.z = +(e.target as any).value)}
				/>
				<input
					type="number"
					bind:value={scale.y}
					step="0.1"
					class:readonly={isUniformScale}
					readonly={isUniformScale}
				/>
				<input
					type="number"
					bind:value={scale.z}
					step="0.1"
					class:readonly={isUniformScale}
					readonly={isUniformScale}
				/>
				<button
					type="button"
					class="tiny-toggle"
					class:active={isUniformScale}
					onclick={() => (isUniformScale = !isUniformScale)}>🔗</button
				>
			</div>
		</div>

		<div class="submit-actions-bottom">
			<button type="submit" class="submit-btn" disabled={isLoading}
				>{isEditing ? 'Update' : 'Add'}</button
			>
			{#if isEditing}<button type="button" onclick={resetForm} class="cancel-button">✖</button>{/if}
		</div>

		<div class="portability-section">
			<div class="portability-grid">
				<button type="button" class="port-btn" onclick={handleExport}>📤 JSON</button>
				<button
					type="button"
					class="port-btn"
					onclick={() => document.getElementById('import-json')?.click()}>📥 JSON</button
				>
				<button type="button" class="port-btn sqlite" onclick={handleExportSQLite}>🗄️ SQL</button>
				<button
					type="button"
					class="port-btn sqlite"
					onclick={() => document.getElementById('import-sqlite')?.click()}>📥 SQL</button
				>
			</div>
			<input
				id="import-json"
				type="file"
				accept=".json"
				style="display:none"
				onchange={(e) => geometryService.importScene((e.target as any).files[0]).then(() => loadGeometries())}
			/>
			<input
				id="import-sqlite"
				type="file"
				accept=".sqlite,.db"
				style="display:none"
				onchange={(e) => geometryService.importScene((e.target as any).files[0]).then(() => loadGeometries())}
			/>
		</div>

		<div class="scene-controls">
			<button
				type="button"
				class="mode-btn toggle"
				class:active={isBloomActive}
				onclick={() => (isBloomActive = !isBloomActive)}>🌸 Bloom</button
			>
			<button
				type="button"
				class="mode-btn toggle"
				class:active={isPremiumActive}
				onclick={() => (isPremiumActive = !isPremiumActive)}>💎 Prem</button
			>
			<button
				type="button"
				class="port-btn sync-db"
				onclick={() =>
					(confirm('Reset ?') && localStorage.removeItem('dv_threlte_geometries_v1')) ||
					window.location.reload()}>🔄 Reset</button
			>
		</div>
	</form>
</div>

<style>
	.form-container {
		width: 100%;
		color: #eee;
		font-size: 0.7rem;
	}
	h3 {
		margin: 0 0 8px 0;
		font-size: 0.8rem;
		color: #4db6ac;
	}
	.upload-container-wrapper {
		background: rgba(0, 0, 0, 0.2);
		border: 1px dashed #444;
		border-radius: 4px;
		padding: 4px;
		margin-bottom: 8px;
	}
	.upload-controls-grid {
		display: grid;
		grid-template-columns: 40px 1fr;
		gap: 8px;
	}
	.upload-zone-compact {
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #222;
		border-radius: 4px;
		cursor: pointer;
		border: 1px solid #333;
	}
	.mini-controls-table {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 4px;
	}
	.tiny-btn {
		padding: 2px 4px;
		font-size: 0.6rem;
		background: #333;
		border: none;
		color: #aaa;
		cursor: pointer;
		border-radius: 2px;
	}
	.tiny-btn.active {
		background: #4db6ac;
		color: #000;
	}
	.tiny-toggle {
		background: #222;
		border: 1px solid #444;
		color: #888;
		padding: 2px 4px;
		cursor: pointer;
		border-radius: 10px;
		font-size: 0.6rem;
	}
	.tiny-toggle.active {
		border-color: #4db6ac;
		color: #4db6ac;
		background: rgba(77, 182, 172, 0.1);
	}

	.geometry-list {
		display: flex;
		flex-direction: column;
		gap: 4px;
		margin-bottom: 8px;
	}
	.custom-dropdown {
		position: relative;
		border: 1px solid #333;
		border-radius: 4px;
		background: #1a1a1a;
	}
	.dropdown-header {
		padding: 4px 8px;
		cursor: pointer;
		font-size: 0.75rem;
		color: #ccc;
	}
	.dropdown-list {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: #111;
		border: 1px solid #333;
		z-index: 10;
		max-height: 150px;
		overflow-y: auto;
	}
	.dropdown-item {
		display: flex;
		align-items: center;
		padding: 4px 8px;
		border-bottom: 1px solid #222;
	}
	.item-name {
		flex: 1;
		cursor: pointer;
	}
	.visibility-toggle {
		background: none;
		border: none;
		cursor: pointer;
		filter: grayscale(1);
	}
	.visibility-toggle.visible {
		filter: none;
	}

	.type-select-row {
		display: grid;
		grid-template-columns: 60px 1fr 30px;
		gap: 4px;
	}
	select,
	input {
		background: #1a1a1a;
		border: 1px solid #333;
		color: #eee;
		padding: 4px;
		border-radius: 4px;
		font-size: 0.7rem;
	}
	.color-input {
		padding: 0;
		height: 24px;
		cursor: pointer;
	}

	.vector-input-row {
		display: grid;
		grid-template-columns: 30px 1fr 1fr 1fr auto;
		gap: 2px;
		align-items: center;
		margin-bottom: 2px;
	}
	.vector-input-row label {
		color: #666;
		font-size: 0.6rem;
	}
	.vector-input-row input {
		padding: 2px;
		text-align: center;
	}
	.readonly {
		opacity: 0.5;
	}

	.submit-actions-bottom {
		display: flex;
		gap: 4px;
		margin-top: 8px;
	}
	.submit-btn {
		flex: 1;
		background: #4db6ac;
		border: none;
		padding: 6px;
		font-weight: bold;
		cursor: pointer;
		border-radius: 4px;
	}
	.cancel-button {
		background: #333;
		border: none;
		color: #fff;
		padding: 0 8px;
		cursor: pointer;
		border-radius: 4px;
	}

	.portability-section {
		margin-top: 8px;
		padding-top: 8px;
		border-top: 1px solid #333;
	}
	.portability-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4px;
	}
	.port-btn {
		padding: 4px;
		font-size: 0.65rem;
		background: #222;
		border: 1px solid #444;
		color: #ddd;
		cursor: pointer;
		border-radius: 4px;
	}
	.port-btn.sqlite {
		color: #4db6ac;
		border-color: #4db6ac;
	}

	.scene-controls {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 4px;
		margin-top: 8px;
	}
	.mode-btn.toggle {
		background: #222;
		border: 1px solid #444;
		color: #555;
		padding: 4px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.65rem;
	}
	.mode-btn.toggle.active {
		border-color: #4db6ac;
		color: #4db6ac;
	}
	.sync-db {
		color: #ef5350 !important;
		border-color: #ef5350 !important;
	}
</style>
