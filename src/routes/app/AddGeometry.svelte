<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { addToast } from '$lib/stores/toasts';
	import { base } from '$app/paths';
	import { geometryService, type GeometryItem } from '$lib/services/api';

	const { selectedGeometry = null } = $props();

	// Utils
	const getRandomValue = (min: number, max: number) => Number(Math.random() * (max - min) + min);
	const formatVal = (val: number) => Number(val.toFixed(2));

	// State (runes)
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
	let portFormat = $state<'json' | 'sqlite'>('sqlite');

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
				const systemTypes = ['box', 'sphere', 'torus', 'icosahedron', 'textmd', 'image_plane'];
				types = [...new Set([...systemTypes, ...(data || []).map((t: any) => t.id)])];
			}
		} catch (error) {
			types = ['box', 'sphere', 'torus', 'textmd'];
		}
	};

	const dispatch = createEventDispatcher();

	const resetForm = () => {
		name = '';
		color = `#${Math.floor(Math.random() * 16777215)
			.toString(16)
			.padStart(6, '0')}`;
		position = { x: 0, y: 0, z: 0 };
		rotation = { x: 0, y: 0, z: 0 };
		scale = { x: 1, y: 1, z: 1 };
		isEditing = false;
		selectedGeometryId = '';
		file = null;
	};

	const loadGeometries = async () => {
		geometries = await geometryService.getAll();
	};

	const handleSubmit = async () => {
		isLoading = true;
		try {
			const formData = new FormData();
			formData.append('name', name || (file ? file.name.split('.')[0] : type));
			formData.append('color', color);
			formData.append('position', JSON.stringify(position));
			formData.append('rotation', JSON.stringify(rotation));
			formData.append('scale', JSON.stringify(scale));

			if (file) {
				formData.append('model_file', file);
				const ext = file.name.split('.').pop()?.toLowerCase() || '';
				formData.append(
					'type',
					['jpg', 'jpeg', 'png', 'webp'].includes(ext) ? 'image_plane' : 'gltf_model'
				);
			} else {
				formData.append('type', type);
			}

			const current = geometries.find((g) => g.id === selectedGeometryId);
			formData.append('visible', String(isEditing && current ? current.visible : true));

			await geometryService.save(formData, isEditing ? selectedGeometryId : undefined);
			addToast(isEditing ? 'Mis à jour !' : 'Ajouté !', 'success');
			if (!isEditing) resetForm();
			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries();
		} catch (error) {
			addToast('Erreur', 'error');
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

	const toggleVisibility = async (id: string) => {
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

	const deleteGeometry = async (id: string) => {
		if (!confirm('Supprimer cet élément ?')) return;
		await geometryService.delete(id);
		if (selectedGeometryId === id) resetForm();
		addToast('Supprimé !', 'success');
		window.dispatchEvent(new Event('modelAdded'));
		await loadGeometries();
	};

	const randomize = (target: 'pos' | 'rot' | 'scl') => {
		if (target === 'pos')
			position = { x: getRandomValue(-5, 5), y: getRandomValue(0, 5), z: getRandomValue(-5, 5) };
		if (target === 'rot')
			rotation = {
				x: getRandomValue(0, 360),
				y: getRandomValue(0, 360),
				z: getRandomValue(0, 360)
			};
		if (target === 'scl') {
			const s = getRandomValue(0.5, 3);
			scale = { x: s, y: s, z: s };
		}
	};

	onMount(() => {
		loadTypes();
		loadGeometries();
		window.addEventListener('directSceneUpload', (e: any) => {
			file = e.detail.file;
			name = file?.name.split('.')[0] || '';
			setTimeout(handleSubmit, 100);
		});
		window.addEventListener('directSceneImport', async (e: any) => {
			await geometryService.importScene(e.detail.file);
			await loadGeometries();
			window.dispatchEvent(new Event('modelAdded'));
		});
		window.addEventListener('manualTransformSync', (e: any) => {
			const d = e.detail;
			if (!d?.id) return;
			if (d.id !== selectedGeometryId) {
				loadGeometryDetails(d.id);
				return;
			}
			if (d.position)
				position = {
					x: formatVal(d.position.x),
					y: formatVal(d.position.y),
					z: formatVal(d.position.z)
				};
			if (d.rotation)
				rotation = {
					x: formatVal(d.rotation.x),
					y: formatVal(d.rotation.y),
					z: formatVal(d.rotation.z)
				};
			if (d.scale)
				scale = { x: formatVal(d.scale.x), y: formatVal(d.scale.y), z: formatVal(d.scale.z) };
			if (d.save) handleSubmit();
		});
	});
</script>

<div class="form-container">
	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleSubmit();
		}}
	>
		<!-- HEADER CONTROLS (PRS + Toggles) -->
		<div class="header-controls">
			<div class="upload-zone" onclick={() => fileInput?.click()} role="button" tabindex="0">
				<input
					bind:this={fileInput}
					type="file"
					accept=".glb,.gltf"
					style="display: none;"
					onchange={(e) => { 
					const t = e.target as HTMLInputElement; if (t.files?.[0]) { file = t.files[0]; name = file.name.split('.')[0]; } 
				}}
				/>
				{file ? '✅' : '📤'}
			</div>

			<div class="modes-grid">
				<div class="prs-row">
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
					<button
						type="button"
						class="tiny-btn gizmo"
						class:active={isTransformControlsEnabled}
						onclick={() => (isTransformControlsEnabled = !isTransformControlsEnabled)}>✜</button
					>
				</div>
				<div class="fx-row">
					<button
						type="button"
						class="fx-btn"
						class:active={isBloomActive}
						onclick={() => (isBloomActive = !isBloomActive)}>🌸</button
					>
					<button
						type="button"
						class="fx-btn"
						class:active={isPremiumActive}
						onclick={() => (isPremiumActive = !isPremiumActive)}>💎</button
					>
					<div class="hand-icon" class:active={isEditing}>✍️</div>
				</div>
			</div>
		</div>

		<!-- DROPDOWN & NAME -->
		<div class="selection-box">
			<div class="custom-dropdown" onmouseleave={() => (isDropdownOpen = false)}>
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
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Filter..."
							onclick={(e) => e.stopPropagation()}
							class="search-input"
						/>
						{#each filteredGeometries as g (g.id)}
							<div class="dropdown-item" class:selected={selectedGeometryId === g.id}>
								<span
									onclick={() => {
										loadGeometryDetails(g.id);
										isDropdownOpen = false;
									}}
									role="button"
									tabindex="0">{g.name}</span
								>
								<div class="item-actions">
									<button
										type="button"
										class:visible={g.visible}
										onclick={() => toggleVisibility(g.id)}>{g.visible ? '👁️' : '🕶️'}</button
									>
									<button type="button" class="del-btn" onclick={() => deleteGeometry(g.id)}
										>🗑️</button
									>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<div class="input-row main">
				<select bind:value={type} class="type-sel">
					{#each types as t}<option value={t}>{t}</option>{/each}
					<option value="text">text</option>
				</select>
				<input type="text" bind:value={name} placeholder="Name" class="name-input" />
				<input type="color" bind:value={color} class="color-input" />
			</div>
		</div>

		<!-- TRANSFORM FIELDS -->
		<div class="transform-area">
			<div class="vec-row">
				<label
					onclick={() => randomize('pos')}
					role="button"
					tabindex="0"
					title="Randomize Position">POS 🎲</label
				>
				<div class="inputs">
					<input type="number" bind:value={position.x} step="0.1" />
					<input type="number" bind:value={position.y} step="0.1" />
					<input type="number" bind:value={position.z} step="0.1" />
				</div>
			</div>
			<div class="vec-row">
				<label
					onclick={() => randomize('rot')}
					role="button"
					tabindex="0"
					title="Randomize Rotation">ROT 🎲</label
				>
				<div class="inputs">
					<input type="number" bind:value={rotation.x} step="1" />
					<input type="number" bind:value={rotation.y} step="1" />
					<input type="number" bind:value={rotation.z} step="1" />
				</div>
			</div>
			<div class="vec-row">
				<label onclick={() => randomize('scl')} role="button" tabindex="0" title="Randomize Scale"
					>SCL 🎲</label
				>
				<div class="inputs">
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
						class="uni-btn"
						class:active={isUniformScale}
						onclick={() => (isUniformScale = !isUniformScale)}
						>{isUniformScale ? '🔗' : '🔓'}</button
					>
				</div>
			</div>
		</div>

		<!-- ACTIONS -->
		<div class="action-footer">
			<button type="submit" class="submit-btn" disabled={isLoading}
				>{isEditing ? 'Update' : 'Add'}</button
			>
			{#if isEditing}<button type="button" onclick={resetForm} class="cancel-btn">✖</button>{/if}
		</div>

		<!-- PORTABILITY -->
		<div class="port-section">
			<div class="port-header">
				<button
					type="button"
					class="format-toggle"
					onclick={() => (portFormat = portFormat === 'json' ? 'sqlite' : 'json')}
				>
					Mode: {portFormat.toUpperCase()}
				</button>
				<div class="port-btns">
					<button
						type="button"
						onclick={() => (portFormat === 'json' ? handleExport() : handleExportSQLite())}
						>� Save</button
					>
					<button type="button" onclick={() => document.getElementById('scene-import')?.click()}
						>📥 Load</button
					>
				</div>
			</div>
			<input
				id="scene-import"
				type="file"
				style="display:none"
				onchange={(e) => geometryService.importScene((e.target as any).files[0]).then(() => loadGeometries())}
			/>
			<button
				type="button"
				class="reset-all"
				onclick={() =>
					(confirm('Reinitialiser la scène ?') &&
						localStorage.removeItem('dv_threlte_geometries_v1')) ||
					window.location.reload()}>🔄 Hard Reset</button
			>
		</div>
	</form>
</div>

<style>
	.form-container {
		width: 100%;
		color: #eee;
		font-family: sans-serif;
	}
	input,
	select,
	button {
		background: #1a1a1a;
		border: 1px solid #333;
		color: #eee;
		border-radius: 4px;
		font-size: 0.65rem;
	}

	.header-controls {
		display: grid;
		grid-template-columns: 44px 1fr;
		gap: 8px;
		margin-bottom: 8px;
	}
	.upload-zone {
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #222;
		border: 1px dashed #555;
		border-radius: 6px;
		cursor: pointer;
		font-size: 1.2rem;
	}

	.modes-grid {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.prs-row,
	.fx-row {
		display: flex;
		gap: 4px;
		align-items: center;
	}
	.tiny-btn,
	.fx-btn {
		flex: 1;
		padding: 4px;
		cursor: pointer;
		border: 1px solid #333;
	}
	.tiny-btn.active,
	.fx-btn.active {
		background: #4db6ac;
		color: #000;
		border-color: #4db6ac;
	}
	.gizmo.active {
		background: #ff9800;
		border-color: #ff9800;
	}
	.hand-icon {
		font-size: 0.8rem;
		opacity: 0.2;
	}
	.hand-icon.active {
		opacity: 1;
		filter: drop-shadow(0 0 5px #4db6ac);
	}

	.selection-box {
		display: flex;
		flex-direction: column;
		gap: 4px;
		margin-bottom: 8px;
	}
	.custom-dropdown {
		position: relative;
		border: 1px solid #333;
		border-radius: 4px;
		background: #111;
	}
	.dropdown-header {
		padding: 4px 8px;
		cursor: pointer;
		color: #4db6ac;
		font-weight: bold;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.dropdown-list {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: #111;
		border: 1px solid #333;
		z-index: 100;
		max-height: 200px;
		overflow-y: auto;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
	}
	.search-input {
		width: 100%;
		padding: 4px;
		border: none;
		border-bottom: 1px solid #333;
		border-radius: 0;
	}
	.dropdown-item {
		display: flex;
		align-items: center;
		padding: 4px 8px;
		border-bottom: 1px solid #222;
	}
	.dropdown-item:hover {
		background: #222;
	}
	.dropdown-item span {
		flex: 1;
		cursor: pointer;
	}
	.item-actions {
		display: flex;
		gap: 4px;
	}
	.item-actions button {
		background: none;
		border: none;
		cursor: pointer;
		padding: 2px;
	}
	.del-btn:hover {
		background: rgba(244, 67, 54, 0.2);
	}

	.input-row.main {
		display: grid;
		grid-template-columns: 70px 1fr 30px;
		gap: 4px;
	}
	.color-input {
		padding: 0;
		height: 100%;
		cursor: pointer;
	}

	.transform-area {
		background: rgba(0, 0, 0, 0.3);
		padding: 6px;
		border-radius: 6px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		margin-bottom: 8px;
	}
	.vec-row {
		display: flex;
		flex-direction: column;
		gap: 2px;
		margin-bottom: 4px;
	}
	.vec-row label {
		font-size: 0.55rem;
		color: #777;
		font-weight: bold;
		cursor: pointer;
		width: fit-content;
	}
	.vec-row label:hover {
		color: #4db6ac;
	}
	.vec-row .inputs {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr auto;
		gap: 2px;
	}
	.vec-row input {
		padding: 3px;
		text-align: center;
	}
	.readonly {
		opacity: 0.3;
	}
	.uni-btn {
		padding: 0 4px;
	}
	.uni-btn.active {
		color: #4db6ac;
		border-color: #4db6ac;
	}

	.action-footer {
		display: flex;
		gap: 4px;
		margin-top: 8px;
	}
	.submit-btn {
		flex: 1;
		background: #4db6ac;
		color: #000;
		font-weight: bold;
		padding: 8px;
		border: none;
		cursor: pointer;
	}
	.cancel-btn {
		background: #333;
		padding: 0 10px;
		cursor: pointer;
	}

	.port-section {
		margin-top: 10px;
		padding-top: 10px;
		border-top: 1px solid #333;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.port-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.format-toggle {
		padding: 2px 6px;
		background: #222;
		color: #888;
		border-color: #444;
	}
	.port-btns {
		display: flex;
		gap: 4px;
	}
	.port-btns button {
		padding: 4px 8px;
		font-weight: bold;
	}
	.reset-all {
		width: 100%;
		margin-top: 4px;
		padding: 4px;
		background: rgba(244, 67, 54, 0.1);
		border-color: rgba(244, 67, 54, 0.3);
		color: #ef5350;
	}
</style>
