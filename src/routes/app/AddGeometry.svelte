<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { addToast } from '$lib/stores/toasts';
	import { base } from '$app/paths';
	import { geometryService, type GeometryItem } from '$lib/services/api';

	const { selectedGeometry = null } = $props();

	// Utils
	const getRandomValue = (min: number, max: number) => Number(Math.random() * (max - min) + min);
	const formatVal = (val: number) => Number(val.toFixed(2));

	// State
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
		if (selectedGeometry && selectedGeometry.id !== selectedGeometryId)
			loadGeometryDetails(selectedGeometry.id);
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
			const res = await fetch(`${base}/data/types.json`);
			if (res.ok) {
				const data = await res.json();
				types = [
					...new Set(['box', 'sphere', 'torus', 'textmd', ...(data || []).map((t: any) => t.id)])
				];
			}
		} catch (e) {
			types = ['box', 'sphere', 'torus', 'textmd'];
		}
	};

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
			const fd = new FormData();
			fd.append('name', name || (file ? file.name.split('.')[0] : type));
			fd.append('color', color);
			fd.append('position', JSON.stringify(position));
			fd.append('rotation', JSON.stringify(rotation));
			fd.append('scale', JSON.stringify(scale));
			if (file) {
				fd.append('model_file', file);
				const ext = file.name.split('.').pop()?.toLowerCase() || '';
				fd.append(
					'type',
					['jpg', 'jpeg', 'png', 'webp'].includes(ext) ? 'image_plane' : 'gltf_model'
				);
			} else fd.append('type', type);

			const current = geometries.find((g) => g.id === selectedGeometryId);
			fd.append('visible', String(isEditing && current ? current.visible : true));

			await geometryService.save(fd, isEditing ? selectedGeometryId : undefined);
			addToast(isEditing ? 'Sync' : 'Added', 'success');
			if (!isEditing) resetForm();
			window.dispatchEvent(new Event('modelAdded'));
			await loadGeometries();
		} catch (e) {
			addToast('Error', 'error');
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
		position = {
			x: formatVal(g.position.x),
			y: formatVal(g.position.y),
			z: formatVal(g.position.z)
		};
		rotation = {
			x: formatVal(g.rotation.x),
			y: formatVal(g.rotation.y),
			z: formatVal(g.rotation.z)
		};
		scale = { x: formatVal(g.scale.x), y: formatVal(g.scale.y), z: formatVal(g.scale.z) };
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
		if (!confirm('Supprimer définitivement cet objet ? 🗑️')) return;
		await geometryService.delete(id);
		if (selectedGeometryId === id) resetForm();
		window.dispatchEvent(new Event('modelAdded'));
		await loadGeometries();
	};

	const randomizeRow = (row: 'pos' | 'rot' | 'scl') => {
		if (row === 'pos')
			position = { x: getRandomValue(-5, 5), y: getRandomValue(0, 5), z: getRandomValue(-5, 5) };
		if (row === 'rot')
			rotation = {
				x: getRandomValue(0, 360),
				y: getRandomValue(0, 360),
				z: getRandomValue(0, 360)
			};
		if (row === 'scl') {
			const s = getRandomValue(0.5, 3);
			scale = { x: s, y: s, z: s };
		}
	};

	const handleExport = () => geometryService.exportScene();
	const handleExportSQLite = () => geometryService.exportSceneToSQLite();

	onMount(() => {
		loadTypes();
		loadGeometries();
		const onDirectUpload = (e: any) => {
			file = e.detail.file;
			name = file?.name.split('.')[0] || '';
			setTimeout(handleSubmit, 100);
		};
		const onDirectImport = async (e: any) => {
			await geometryService.importScene(e.detail.file);
			await loadGeometries();
			window.dispatchEvent(new Event('modelAdded'));
		};
		const onSync = (e: any) => {
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
		};
		window.addEventListener('directSceneUpload', onDirectUpload);
		window.addEventListener('directSceneImport', onDirectImport);
		window.addEventListener('manualTransformSync', onSync);
		return () => {
			window.removeEventListener('directSceneUpload', onDirectUpload);
			window.removeEventListener('directSceneImport', onDirectImport);
			window.removeEventListener('manualTransformSync', onSync);
		};
	});
</script>

<div class="form-container">
	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleSubmit();
		}}
		ondragover={(e) => {
			e.preventDefault();
			isDragging = true;
		}}
		ondragleave={() => (isDragging = false)}
		ondrop={(e) => {
			e.preventDefault();
			isDragging = false;
			if (e.dataTransfer?.files[0]) {
				file = e.dataTransfer.files[0];
				name = file.name.split('.')[0];
				setTimeout(handleSubmit, 100);
			}
		}}
		class:dragging={isDragging}
	>
		<div class="top-bar">
			<div class="upload-btn" onclick={() => fileInput?.click()} role="button" tabindex="0">
				<input
					bind:this={fileInput}
					type="file"
					accept=".glb,.gltf"
					style="display: none;"
					onchange={(e: any) => {
						if (e.target.files[0]) {
							file = e.target.files[0];
							name = file.name.split('.')[0];
						}
					}}
				/>
				{file ? '✅' : '📤'}
			</div>

			<div class="tiny-controls-group">
				<div class="btn-row">
					<button
						type="button"
						class:active={transformModes.includes('translate')}
						onclick={() => (transformModes = ['translate'])}>P</button
					>
					<button
						type="button"
						class:active={transformModes.includes('rotate')}
						onclick={() => (transformModes = ['rotate'])}>R</button
					>
					<button
						type="button"
						class:active={transformModes.includes('scale')}
						onclick={() => (transformModes = ['scale'])}>S</button
					>
					<button
						type="button"
						class="gizmo"
						class:active={isTransformControlsEnabled}
						onclick={() => (isTransformControlsEnabled = !isTransformControlsEnabled)}>✜</button
					>
				</div>
				<div class="btn-row">
					<button
						type="button"
						class:active={isBloomActive}
						onclick={() => (isBloomActive = !isBloomActive)}>🌸</button
					>
					<button
						type="button"
						class:active={isPremiumActive}
						onclick={() => (isPremiumActive = !isPremiumActive)}>💎</button
					>
					<div class="edit-marker" class:active={isEditing}>✍️</div>
				</div>
			</div>
		</div>

		<div class="selection-row">
			<div class="custom-dropdown" onmouseleave={() => (isDropdownOpen = false)}>
				<div
					class="dropdown-header"
					onclick={() => (isDropdownOpen = !isDropdownOpen)}
					onmouseenter={() => (isDropdownOpen = true)}
					role="button"
					tabindex="0"
				>
					{selectedGeometryId
						? geometries.find((g) => g.id === selectedGeometryId)?.name
						: '-- List --'}
				</div>
				{#if isDropdownOpen}
					<div class="dropdown-list">
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Filter..."
							onclick={(e) => e.stopPropagation()}
						/>
						{#each filteredGeometries as g (g.id)}
							<div class="item" class:selected={selectedGeometryId === g.id}>
								<span
									onclick={() => {
										loadGeometryDetails(g.id);
										isDropdownOpen = false;
									}}
									role="button"
									tabindex="0">{g.name}</span
								>
								<div class="acts">
									<button type="button" onclick={() => toggleVisibility(g.id)}
										>{g.visible ? '👁️' : '🕶️'}</button
									>
									<button type="button" class="del" onclick={() => deleteGeometry(g.id)}>🗑️</button>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>

		<div class="name-type-row">
			<select bind:value={type}>
				{#each types as t}<option value={t}>{t}</option>{/each}
				<option value="text">text</option>
			</select>
			<input type="text" bind:value={name} placeholder="Name" />
			<input type="color" bind:value={color} />
		</div>

		<div class="transform-rows">
			<div class="row">
				<label onclick={() => randomizeRow('pos')} role="button" tabindex="0">POS</label>
				<input
					type="number"
					bind:value={position.x}
					step="0.01"
					oninput={(e: any) => (position.x = formatVal(+e.target.value))}
				/>
				<input
					type="number"
					bind:value={position.y}
					step="0.01"
					oninput={(e: any) => (position.y = formatVal(+e.target.value))}
				/>
				<input
					type="number"
					bind:value={position.z}
					step="0.01"
					oninput={(e: any) => (position.z = formatVal(+e.target.value))}
				/>
			</div>
			<div class="row">
				<label onclick={() => randomizeRow('rot')} role="button" tabindex="0">ROT</label>
				<input
					type="number"
					bind:value={rotation.x}
					step="1"
					oninput={(e: any) => (rotation.x = formatVal(+e.target.value))}
				/>
				<input
					type="number"
					bind:value={rotation.y}
					step="1"
					oninput={(e: any) => (rotation.y = formatVal(+e.target.value))}
				/>
				<input
					type="number"
					bind:value={rotation.z}
					step="1"
					oninput={(e: any) => (rotation.z = formatVal(+e.target.value))}
				/>
			</div>
			<div class="row">
				<label onclick={() => randomizeRow('scl')} role="button" tabindex="0">SCL</label>
				<input
					type="number"
					bind:value={scale.x}
					step="0.01"
					oninput={(e: any) => {
						const v = formatVal(+e.target.value);
						scale.x = v;
						if (isUniformScale) {
							scale.y = v;
							scale.z = v;
						}
					}}
				/>
				<input
					type="number"
					bind:value={scale.y}
					step="0.01"
					class:readonly={isUniformScale}
					readonly={isUniformScale}
					oninput={(e: any) => (scale.y = formatVal(+e.target.value))}
				/>
				<input
					type="number"
					bind:value={scale.z}
					step="0.01"
					class:readonly={isUniformScale}
					readonly={isUniformScale}
					oninput={(e: any) => (scale.z = formatVal(+e.target.value))}
				/>
				<button
					type="button"
					class="lock"
					class:active={isUniformScale}
					onclick={() => (isUniformScale = !isUniformScale)}>{isUniformScale ? '🔗' : '🔓'}</button
				>
			</div>
		</div>

		<div class="bottom-actions">
			<button type="submit" class="main-btn" disabled={isLoading}
				>{isEditing ? 'SYNC' : 'ADD'}</button
			>
			{#if isEditing}<button type="button" class="cancel-btn" onclick={resetForm}>✖</button>{/if}
		</div>

		<div class="extra-footer">
			<div class="port-tools">
				<button
					type="button"
					class="fmt"
					onclick={() => (portFormat = portFormat === 'json' ? 'sqlite' : 'json')}
					>{portFormat.toUpperCase()}</button
				>
				<button
					type="button"
					onclick={() => (portFormat === 'json' ? handleExport() : handleExportSQLite())}
					title="Save">💾</button
				>
				<button
					type="button"
					onclick={() => document.getElementById('scene-import')?.click()}
					title="Open">📂</button
				>
				<button
					type="button"
					class="reset-btn"
					onclick={() =>
						(confirm('Hard Reset Scene?') && localStorage.removeItem('dv_threlte_geometries_v1')) ||
						window.location.reload()}
					title="Reset">🔄</button
				>
			</div>
		</div>
	</form>
</div>

<style>
	.form-container {
		font-size: 0.6rem;
		color: #ddd;
	}
	button,
	input,
	select {
		background: #111;
		border: 1px solid #333;
		color: #eee;
		border-radius: 2px;
		font-size: 0.6rem;
		padding: 2px;
	}
	button {
		cursor: pointer;
	}
	form.dragging {
		background: rgba(77, 182, 172, 0.2);
		border: 1px dashed #4db6ac;
	}

	.top-bar {
		display: flex;
		justify-content: space-between;
		margin-bottom: 6px;
	}
	.upload-btn {
		width: 30px;
		height: 30px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #222;
		border: 1px dashed #444;
		border-radius: 4px;
		font-size: 1rem;
	}

	.tiny-controls-group {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.btn-row {
		display: flex;
		gap: 2px;
		justify-content: flex-end;
	}
	.btn-row button {
		width: 18px;
		height: 18px;
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.55rem;
	}
	.btn-row button.active {
		background: #4db6ac;
		color: #000;
		border-color: #4db6ac;
	}
	.gizmo.active {
		background: #ff9800 !important;
		border-color: #ff9800 !important;
	}
	.edit-marker {
		font-size: 0.7rem;
		opacity: 0.2;
	}
	.edit-marker.active {
		opacity: 1;
		filter: drop-shadow(0 0 3px #4db6ac);
	}

	.selection-row {
		margin-bottom: 4px;
	}
	.custom-dropdown {
		position: relative;
		width: 100%;
		background: #111;
		border: 1px solid #333;
	}
	.dropdown-header {
		padding: 3px 6px;
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
		background: #0a0a0a;
		border: 1px solid #333;
		z-index: 100;
		max-height: 150px;
		overflow-y: auto;
	}
	.dropdown-list input {
		width: 100%;
		border: none;
		border-bottom: 1px solid #222;
	}
	.item {
		display: flex;
		align-items: center;
		padding: 2px 6px;
		border-bottom: 1px solid #111;
	}
	.item span {
		flex: 1;
		cursor: pointer;
	}
	.acts {
		display: flex;
		gap: 2px;
	}
	.acts button {
		border: none;
		background: none;
	}
	.del:hover {
		color: #f44336;
	}

	.name-type-row {
		display: grid;
		grid-template-columns: 50px 1fr 20px;
		gap: 2px;
		margin-bottom: 4px;
	}

	.transform-rows {
		display: flex;
		flex-direction: column;
		gap: 2px;
		background: rgba(0, 0, 0, 0.2);
		padding: 4px;
		border-radius: 4px;
		margin-bottom: 4px;
	}
	.row {
		display: grid;
		grid-template-columns: 25px 1fr 1fr 1fr auto;
		gap: 2px;
		align-items: center;
	}
	.row label {
		font-size: 0.5rem;
		color: #666;
		cursor: pointer;
		font-weight: bold;
	}
	.row input {
		width: 100%;
		text-align: center;
	}
	.readonly {
		opacity: 0.3;
	}
	.lock.active {
		color: #4db6ac;
		border-color: #4db6ac;
	}

	.bottom-actions {
		display: flex;
		gap: 2px;
	}
	.main-btn {
		flex: 1;
		background: #4db6ac;
		color: #000;
		font-weight: bold;
		border: none;
		padding: 4px;
	}
	.cancel-btn {
		width: 25px;
		background: #333;
		border: none;
	}

	.extra-footer {
		margin-top: 6px;
		border-top: 1px solid #222;
		padding-top: 4px;
	}
	.port-tools {
		display: flex;
		gap: 2px;
		align-items: center;
	}
	.port-tools button {
		flex: 1;
		font-weight: bold;
		font-size: 0.6rem;
	}
	.fmt {
		color: #888;
		flex: 1.5 !important;
	}
	.reset-btn {
		color: #ef5350;
		border-color: rgba(244, 67, 54, 0.4);
		background: rgba(244, 67, 54, 0.05);
	}
	.reset-btn:hover {
		background: rgba(244, 67, 54, 0.2);
	}
</style>
