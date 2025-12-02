<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { addToast } from '$lib/stores/toasts';

  const { selectedGeometry = null } = $props();

  $effect(() => {
    if (selectedGeometry && selectedGeometry.id !== selectedGeometryId) {
      loadGeometryDetails(selectedGeometry.id);
    }
  });

  const getRandomValue = (min: number, max: number) => Number(Math.random() * (max - min) + min).toFixed(2);

  // State for the form (runes)
  let name = $state(''); 
  let type = $state('box'); 
  let color = $state(`#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`); 
  let position = $state({ x: 0, y: 0, z: 0 }); 
  let rotation = $state({ x: Number(getRandomValue(0, 360)), y: Number(getRandomValue(0, 360)), z: Number(getRandomValue(0, 360)) });
  let file: File | null = $state(null); // State for the uploaded file
  
  let geometries = $state([]);
  let selectedGeometryId = $state('');
  let isEditing = $state(false);
  let types = $state([]);
  let isLoading = $state(false);

  const loadTypes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/types/');
      if (!response.ok) throw new Error('Failed to fetch types');
      const data = await response.json();
      types = data.map(type => type.id);
    } catch (error) {
      console.error('Error loading types:', error);
      addToast('Failed to load types. Please try again.', 'error');
    }
  };

  const dispatch = createEventDispatcher();

  const resetForm = () => {
    type = types.length > 0 ? types[Math.floor(Math.random() * types.length)] : 'box';
    name = type;
    color = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
    position = { x: Number(getRandomValue(-5, 5)), y: Number(getRandomValue(-5, 5)), z: Number(getRandomValue(-5, 5)) };
    rotation = { x: Number(getRandomValue(0, 360)), y: Number(getRandomValue(0, 360)), z: Number(getRandomValue(0, 360)) };
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
      const response = await fetch('http://localhost:8000/api/geometries/');
      if (!response.ok) throw new Error('Failed to fetch geometries');
      geometries = (await response.json()).results || [];
    } catch (error) {
      console.error('Error loading geometries:', error);
      addToast('Failed to load geometries. Please try again.', 'error');
    }
  };

  const handleSubmit = async () => {
    isLoading = true;
    try {
      // Si un fichier est sélectionné, utiliser la logique d'upload
      if (file) {
        const formData = new FormData();
        const randomId = Math.random().toString(36).substring(2, 7);
        const uniqueName = `${name || file.name}-${randomId}`;
        const modelType = file.name.split('.').pop()?.toLowerCase();

        formData.append('model_file', file);
        formData.append('name', uniqueName);
        formData.append('type', 'gltf_model');
        formData.append('color', color);
        formData.append('position', JSON.stringify(position));
        formData.append('rotation', JSON.stringify(rotation));
        if (modelType) formData.append('model_type', modelType);

        const response = await fetch('/api/geometries/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.name?.[0] || errorData.detail || 'Upload failed');
        }
        addToast('Model uploaded successfully!', 'success');

      } else { // Sinon, utiliser la logique pour les formes de base
        const randomId = Math.random().toString(36).substring(2, 7);
        const uniqueName = isEditing ? name : `${name}-${randomId}`;
        const geometry = { name: uniqueName, type, color, position, rotation };
        
        let url = 'http://localhost:8000/api/geometries/';
        let method = 'POST';
        if (isEditing && selectedGeometryId) {
          url = `${url}${selectedGeometryId}/`;
          method = 'PUT';
        }
        
        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(geometry),
        });

        if (!response.ok) {
          const errorBody = await response.json();
          throw new Error(errorBody.name?.[0] || (isEditing ? 'Failed to update geometry' : 'Failed to add geometry'));
        }
        addToast(isEditing ? 'Geometry updated!' : 'Geometry added!', 'success');
      }

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
      const response = await fetch(`http://localhost:8000/api/geometries/${selectedGeometryId}/`, {
        method: 'DELETE',
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
      const response = await fetch(`/api/geometries/${id}/`);
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
  <form onsubmit={(event) => { event.preventDefault(); handleSubmit(); }}>
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
      <input id="file-upload" type="file" accept=".glb,.gltf" onchange={(e) => file = e.target.files?.[0] || null} />
      {#if file}
        <p>Selected file: {file.name}</p>
      {/if}
    </div>

    <button type="submit" class={isEditing ? 'update-button' : 'add-button'} disabled={isLoading}>
      {isLoading ? 'Saving...' : (isEditing ? 'Update' : 'Add')}
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
  /* Styles are omitted for brevity, assuming they are complex and unchanged */
</style>

