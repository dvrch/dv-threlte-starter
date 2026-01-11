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
	const getNextName = (base: string) => {
		let n = base;
		let i = 1;
		while (geometries.some((g) => g.name === n)) {
			n = `${base} ${i++}`;
		}
		return n;
	};

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
	const portFormats: ('sqlite' | 'json' | 'csv')[] = ['sqlite', 'json', 'csv'];

	// State & Persistence
	const savedSettings = geometryService.getSettings();

	let isBloomActive = $state(savedSettings.isBloomActive);
	let isPremiumActive = $state(savedSettings.isPremiumActive);
	let isTransformControlsEnabled = $state(savedSettings.isTransformControlsEnabled);
	let transformModes = $state<('translate' | 'rotate' | 'scale')[]>(savedSettings.transformModes);
	let searchQuery = $state(savedSettings.searchQuery);
	let portFormatIndex = $state(
		portFormats.indexOf(savedSettings.portFormat as any) === -1
			? 0
			: portFormats.indexOf(savedSettings.portFormat as any)
	);
	let portFormat = $derived(portFormats[portFormatIndex]);

	let importURL = $state('');
	let selectedIds = $state<Set<string>>(new Set());

	let filteredGeometries = $derived(
		geometries.filter((g) => g.name.toLowerCase().includes(searchQuery.toLowerCase()))
	);

	// Multi-select actions
	const toggleInBulk = (id: string) => {
		const newSet = new Set(selectedIds);
		if (newSet.has(id)) newSet.delete(id);
		else newSet.add(id);
		selectedIds = newSet;
	};

	const bulkDelete = async () => {
		if (selectedIds.size === 0 || !confirm(`Supprimer ${selectedIds.size} objets ?`)) return;
		for (const id of selectedIds) await geometryService.delete(id);
		selectedIds = new Set();
		await loadGeometries();
		window.dispatchEvent(new Event('modelAdded'));
	};

	const bulkHide = async () => {
		for (const id of selectedIds) await toggleVisibility(id, false);
		selectedIds = new Set();
	};

	const handleURLImport = async () => {
		if (!importURL) return;
		isLoading = true;
		try {
			const fd = new FormData();
			const rawName = importURL.split('/').pop()?.split('?')[0] || 'Imported';
			fd.append('name', getNextName(rawName.split('.')[0]));
			fd.append('model_url', importURL);
			const isImg = /\.(jpg|jpeg|png|webp|gif)$/i.test(importURL);
			fd.append('type', isImg ? 'image_plane' : 'gltf_model');
			fd.append('position', JSON.stringify({ x: 0, y: 0, z: 0 }));
			fd.append('rotation', JSON.stringify({ x: 0, y: 0, z: 0 }));
			fd.append('scale', JSON.stringify({ x: 1, y: 1, z: 1 }));
			await geometryService.save(fd);
			importURL = '';
			await loadGeometries();
			window.dispatchEvent(new Event('modelAdded'));
			addToast('Imported from URL', 'success');
		} catch (e) {
			addToast('URL Error', 'error');
		} finally {
			isLoading = false;
		}
	};

	// ⚙️ Persistance des réglages
	$effect(() => {
		geometryService.saveSettings({
			isBloomActive,
			isPremiumActive,
			isTransformControlsEnabled,
			transformModes,
			portFormat,
			searchQuery
		});
	});

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
			const finalName = isEditing
				? name
				: getNextName(name || (file ? file.name.split('.')[0] : type));
			fd.append('name', finalName);
			fd.append('color', color);
			fd.append('position', JSON.stringify(position));
			fd.append('rotation', JSON.stringify(rotation));
			fd.append('scale', JSON.stringify(scale));
			if (file) {
				fd.append('model_file', file);
				const ext = file.name.split('.').pop()?.toLowerCase() || '';
				const isImage = ['jpg', 'jpeg', 'png', 'webp'].includes(ext);
				if (isEditing) {
					fd.append('type', type);
				} else {
					fd.append('type', isImage ? 'image_plane' : 'gltf_model');
				}
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

	const toggleVisibility = async (id: string, force?: boolean) => {
		const g = geometries.find((g) => g.id === id);
		if (!g) return;
		const next = force !== undefined ? force : !g.visible;
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
			const f = e.detail.file;
			if (!f) return;

			const ext = f.name.split('.').pop()?.toLowerCase() || '';
			// Si c'est un fichier de scène, on le redirige vers l'import
			if (['csv', 'json', 'sqlite'].includes(ext)) {
				onDirectImport(e);
				return;
			}

			file = f;
			name = f.name.split('.')[0] || '';
			setTimeout(handleSubmit, 100);
		};
		const onDirectImport = async (e: any) => {
			await geometryService.importScene(e.detail.file);
			await loadGeometries();
			window.dispatchEvent(new Event('modelAdded'));
			window.dispatchEvent(new Event('sceneUpdated'));
		};
		const onMarkdownUpload = (e: any) => {
			const finalName = getNextName(e.detail.name);
			const fd = new FormData();
			fd.append('name', finalName);
			fd.append('type', 'textmd'); // Type explicite
			fd.append('color', color);
			fd.append('position', JSON.stringify({ x: 0, y: 5, z: 0 }));
			fd.append('rotation', JSON.stringify({ x: 0, y: 0, z: 0 }));
			fd.append('scale', JSON.stringify({ x: 1, y: 1, z: 1 }));
			fd.append('markdown_content', e.detail.content);

			geometryService.save(fd).then(() => {
				addToast('Markdown 3D Ready', 'success');
				loadGeometries();
				window.dispatchEvent(new Event('modelAdded'));
			});
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
		window.addEventListener('markdownUpload', onMarkdownUpload);
		window.addEventListener('manualTransformSync', onSync);
		return () => {
			window.removeEventListener('directSceneUpload', onDirectUpload);
			window.removeEventListener('directSceneImport', onDirectImport);
			window.removeEventListener('markdownUpload', onMarkdownUpload);
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
		<!-- 1. Hiérarchie Inversée : Contrôles en haut -->
		<div class="selection-row">
			<div
				class="custom-dropdown"
				onmouseenter={() => (isDropdownOpen = true)}
				onmouseleave={() => (isDropdownOpen = false)}
			>
				<div class="dropdown-header">
					<span class="selected-label">
						{selectedIds.size > 0
							? `${selectedIds.size} selected`
							: selectedGeometryId
							? geometries.find((g) => g.id === selectedGeometryId)?.name
							: '-- Objects --'}
					</span>
					<div class="bulk-tools">
						{#if selectedIds.size > 0}
							<button type="button" class="bulk-btn del" onclick={bulkDelete}>🗑️</button>
							<button type="button" class="bulk-btn hide" onclick={bulkHide}>🕶️</button>
						{/if}
						<div class="dropdown-trigger" onclick={() => (isDropdownOpen = !isDropdownOpen)}>
							<span class="chevron" class:open={isDropdownOpen}>V</span>
						</div>
					</div>
				</div>
				{#if isDropdownOpen}
					<div class="dropdown-list">
						<div class="top-list">
							<input
								type="text"
								bind:value={searchQuery}
								placeholder="Filter..."
								onclick={(e) => e.stopPropagation()}
							/>
							<input
								type="text"
								bind:value={importURL}
								placeholder="URL..."
								onclick={(e) => e.stopPropagation()}
								onkeydown={(e) => e.key === 'Enter' && handleURLImport()}
							/>
						</div>

						<div class="scroll-list">
							{#each filteredGeometries as g (g.id)}
								<div
									class="item"
									class:selected={selectedGeometryId === g.id}
									class:multi={selectedIds.has(g.id)}
								>
									<input
										type="checkbox"
										checked={selectedIds.has(g.id)}
										onclick={(e) => {
											e.stopPropagation();
											toggleInBulk(g.id);
										}}
									/>
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
										<button type="button" class="del" onclick={() => deleteGeometry(g.id)}
											>🗑️</button
										>
									</div>
								</div>
							{:else}
								<div class="empty-list">No objects found</div>
							{/each}
						</div>
					</div>
				{/if}
			</div>
		</div>

		<div class="transform-rows">
			<div class="row">
				<label onclick={() => randomizeRow('pos')} role="button" tabindex="0">P</label>
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
				<label onclick={() => randomizeRow('rot')} role="button" tabindex="0">R</label>
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
				<label onclick={() => randomizeRow('scl')} role="button" tabindex="0">S</label>
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

		<div class="name-type-row">
			<select bind:value={type}>
				{#each types as t}<option value={t}>{t}</option>{/each}
				<option value="text">text</option>
			</select>
			<input type="text" bind:value={name} placeholder="Name" />
			<input type="color" bind:value={color} />
		</div>

		<div class="bottom-actions">
			<div class="extra-btns">
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
				<button
					type="button"
					class="gizmo"
					class:active={isTransformControlsEnabled}
					onclick={() => (isTransformControlsEnabled = !isTransformControlsEnabled)}
					title="Toggle Gizmo (Hand)"
				>
					{isEditing ? '✍️' : '🤚'}
				</button>
			</div>

			<div class="main-btns">
				{#if isEditing}<button type="button" class="cancel-btn" onclick={resetForm}>✖</button>{/if}
				<button type="submit" class="main-btn" disabled={isLoading}
					>{isEditing ? 'SYNC' : 'ADD'}</button
				>
			</div>
		</div>

		<!-- 2. Status & Upload en bas -->
		<div class="footer-zone">
			<div class="upload-btn" onclick={() => fileInput?.click()} role="button" tabindex="0">
				<input
					bind:this={fileInput}
					type="file"
					accept=".glb,.gltf"
					style="display: none;"
					onchange={(e: any) => {
						const f = e.target.files[0];
						if (f) {
							file = f;
							name = f.name.split('.')[0];
						}
					}}
				/>
				{file ? '✅' : '📤'}
			</div>

			<div class="port-tools">
				<button
					type="button"
					class="fmt"
					onclick={() => (portFormatIndex = (portFormatIndex + 1) % portFormats.length)}
					>{portFormat.toUpperCase()}</button
				>
				<button
					type="button"
					onclick={() => {
						if (portFormat === 'json') handleExport();
						else if (portFormat === 'sqlite') handleExportSQLite();
						else if (portFormat === 'csv') geometryService.exportSceneToCSV();
					}}
					title="Save">💾</button
				>
				<button
					type="button"
					onclick={() => document.getElementById('scene-import')?.click()}
					title="Open">📂</button
				>
				<button
					type="button"
					onclick={() => window.dispatchEvent(new Event('requestSceneExportGLB'))}
					title="Export GLB"
					style="color: #4db6ac; border-color: #4db6ac;">📦</button
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
		<input
			id="scene-import"
			type="file"
			accept=".json,.sqlite,.db,.csv"
			style="display:none"
			onchange={async (e) => {
				const f = (e.target as any).files[0];
				if (f) {
					await geometryService.importScene(f);
					await loadGeometries();
					window.dispatchEvent(new Event('modelAdded'));
				}
			}}
		/>
	</form>
</div>

<style>
	.form-container {
		position: fixed;
		bottom: 10px;
		right: 10px;
		width: 170px;
		font-size: 0.55rem;
		color: #ddd;
		background: rgba(10, 10, 10, 0.95);
		backdrop-filter: blur(10px);
		border: 1px solid #333;
		border-radius: 8px;
		padding: 6px;
		z-index: 1000;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
	}
	button,
	input,
	select {
		background: #111;
		border: 1px solid #333;
		color: #eee;
		border-radius: 2px;
		font-size: 0.55rem;
		padding: 2px;
	}
	button {
		cursor: pointer;
	}
	form {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.footer-zone {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 4px;
		border-top: 1px solid #222;
	}

	.upload-btn {
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #222;
		border: 1px dashed #444;
		border-radius: 4px;
		font-size: 0.8rem;
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
		display: flex;
		justify-content: space-between;
		align-items: center;
		color: #4db6ac;
		font-weight: bold;
		white-space: nowrap;
		height: 22px;
	}
	.selected-label {
		padding: 0 6px;
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.dropdown-trigger {
		width: 20px;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.03);
		border-left: 1px solid #222;
		cursor: pointer;
	}
	.chevron {
		font-size: 0.5rem;
		transition: transform 0.2s;
		display: inline-block;
	}
	.chevron.open {
		transform: rotate(180deg);
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
	.bulk-tools {
		display: flex;
		align-items: center;
		gap: 4px;
		padding-right: 4px;
	}
	.bulk-btn {
		font-size: 0.7rem;
		padding: 0 4px;
		border-radius: 4px;
		height: 18px;
		background: #222;
		border: 1px solid #444;
	}
	.bulk-btn.del:hover {
		background: #b71c1c;
		color: white;
		border-color: #f44336;
	}
	.bulk-btn.hide:hover {
		background: #455a64;
		color: white;
	}

	.top-list {
		display: flex;
		flex-direction: column;
		background: #111;
		border-bottom: 2px solid #222;
	}
	.top-list input {
		height: 20px;
		background: #000;
	}

	.scroll-list {
		max-height: 250px;
		overflow-y: auto;
	}

	.item {
		display: flex;
		align-items: center;
		padding: 2px 6px;
		border-bottom: 1px solid #111;
		gap: 6px;
	}
	.item.multi {
		background: rgba(77, 182, 172, 0.1);
	}
	.item input[type='checkbox'] {
		width: 10px;
		height: 10px;
		cursor: pointer;
	}
	.item span {
		flex: 1;
		cursor: pointer;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.acts {
		display: flex;
		gap: 2px;
	}
	.acts button {
		border: none;
		background: none;
		opacity: 0.6;
	}
	.acts button:hover {
		opacity: 1;
	}
	.del:hover {
		color: #f44336;
	}
	.empty-list {
		padding: 10px;
		text-align: center;
		opacity: 0.5;
	}

	.bottom-actions {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 4px;
	}
	.extra-btns {
		display: flex;
		gap: 2px;
	}
	.extra-btns button {
		width: 20px;
		height: 20px;
	}
	.main-btns {
		display: flex;
		gap: 2px;
	}
	.main-btn {
		background: #4db6ac;
		color: #000;
		font-weight: bold;
		padding: 2px 10px;
	}
	.cancel-btn {
		color: #f44336;
	}

	.name-type-row {
		display: grid;
		grid-template-columns: 45px 1fr 20px;
		gap: 2px;
	}

	.transform-rows {
		display: flex;
		flex-direction: column;
		gap: 2px;
		background: rgba(255, 255, 255, 0.03);
		padding: 4px;
		border-radius: 4px;
	}
	.row {
		display: grid;
		grid-template-columns: 20px 1fr 1fr 1fr auto;
		gap: 2px;
		align-items: center;
	}
	.row label {
		font-size: 0.5rem;
		color: #4db6ac;
		cursor: pointer;
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

	.port-tools {
		display: flex;
		gap: 2px;
		align-items: center;
		flex: 1;
	}
	.port-tools button {
		flex: 1;
		font-weight: bold;
		padding: 2px;
	}
	.fmt {
		color: #888;
	}
	.reset-btn {
		color: #ef5350;
	}
	.item.selected span {
		color: #fff;
		text-shadow: 0 0 5px #4db6ac;
	}
</style>
