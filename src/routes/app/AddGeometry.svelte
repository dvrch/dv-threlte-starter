<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { Sphere } from 'three';
  import { addToast } from '$lib/stores/toasts';

  export let selectedGeometry: any = null;

  $: if (selectedGeometry && selectedGeometry.id !== selectedGeometryId) {
    loadGeometryDetails(selectedGeometry.id);
  }

  const getRandomValue = (min: number, max: number) => Number(Math.random() * (max - min) + min).toFixed(2);


  let name = ''; 
  let type = 'box'; 
  // let color = '#0059BA'; 
  let color = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`; 
  let position = { x: 0, y: 0, z: 0 }; 
  let rotation = { x: Number(getRandomValue(0, 360)), y: Number(getRandomValue(0, 360)), z: Number(getRandomValue(0, 360)) };
  // champs optionnels pour les modèles uploadés
  let model_url: string = '';
  let model_type: string = '';
  let geometries = [];
  let selectedGeometryId = '';
  let isEditing = false;
  let types = [];
  
  // const types = await fetch('http://localhost:8000/api/types/').then(res => res.json());
  const loadTypes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/types/');
      if (!response.ok) {
        throw new Error('Failed to fetch types');
      }

      const data = await response.json();
      types = data.map(type => type.id);
    } catch (error) {
      console.error('Error loading types:', error);
      addToast('Failed to load types. Please try again.', 'error');
    }
  };


  const dispatch = createEventDispatcher();

  const resetForm = () => {
    type = types[Math.floor(Math.random() * types.length)];
    name = type;
    color = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
    position = { x: Number(getRandomValue(-5, 5)), y: Number(getRandomValue(-5, 5)), z: Number(getRandomValue(-5, 5)) };
    rotation = { x: Number(getRandomValue(0, 360)), y: Number(getRandomValue(0, 360)), z: Number(getRandomValue(0, 360)) };
    isEditing = false;
    selectedGeometryId = '';
  };

  onMount(() => {
    (async () => {
      await loadTypes();
      await loadGeometries();
      resetForm();
    })();
    const handleUploaded = (e: any) => {
      if (e?.detail?.url) {
        model_url = e.detail.url;
        model_type = e.detail.model_type || '';
        name = e.detail.filename || name;
      }
    };
    window.addEventListener('modelUploaded', handleUploaded as EventListener);
    return () => {
      window.removeEventListener('modelUploaded', handleUploaded as EventListener);
    };
  });

  const loadGeometries = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/geometries/');
      if (!response.ok) {
        throw new Error('Failed to fetch geometries');
      }
      geometries = (await response.json()).results || [];
    } catch (error) {
      console.error('Error loading geometries:', error);
      addToast('Failed to load geometries. Please try again.', 'error');
    }
  };

  const updateGeometry = async () => {
    try {
      const geometry = { name, type, color, position, rotation, model_url, model_type };
      const response = await fetch(`http://localhost:8000/api/geometries/${selectedGeometryId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(geometry),
      });

      if (!response.ok) {
        throw new Error('Failed to update geometry');
      }

      const result = await response.json();
      console.log('Updated geometry:', result);
      
      dispatch('geometryChanged');
      window.dispatchEvent(new Event('geometryChanged'));
      addToast('Geometry updated successfully!', 'success');
      
      // Ne pas réinitialiser le formulaire après la mise à jour
      // pour permettre d'autres modifications si nécessaire
    } catch (error) {
      console.error('Error updating geometry:', error);
      addToast('Failed to update geometry. Please try again.', 'error');
    }
  };

  const addGeometry = async () => {
    try {
      const geometry = { name, type, color, position, rotation, model_url, model_type };
      const response = await fetch('http://localhost:8000/api/geometries/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(geometry),
      });

      if (!response.ok) {
        throw new Error('Failed to add geometry');
      }

      const result = await response.json();
      console.log('Added geometry:', result);
      
      resetForm();
      dispatch('geometryChanged');
      window.dispatchEvent(new Event('geometryChanged'));
      addToast('Geometry added successfully!', 'success');
      // notifier globalement pour rafraîchir la scène
      window.dispatchEvent(new CustomEvent('modelAdded'))
    } catch (error) {
      console.error('Error adding geometry:', error);
      addToast('Failed to add geometry. Please try again.', 'error');
    }
  };

  const handleSubmit = async () => {
    const geometry = { name, type, color, position, rotation };
    
    try {
      let response;
      let url = 'http://localhost:8000/api/geometries/';
      let method = 'POST';
      
      if (isEditing && selectedGeometryId) {
        url = `${url}${selectedGeometryId}/`;
        method = 'PUT';
      }
      
      response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(geometry),
      });

      if (!response.ok) {
        throw new Error(isEditing ? 'Failed to update geometry' : 'Failed to add geometry');
      }

      const result = await response.json();
      console.log(isEditing ? 'Updated geometry:' : 'Added geometry:', result);
      
      if (!isEditing) {
        resetForm(); // Réinitialiser seulement pour un nouvel ajout
      }
      
      dispatch('geometryChanged');
      addToast(isEditing ? 'Geometry updated successfully!' : 'Geometry added successfully!', 'success');
    } catch (error) {
      console.error(isEditing ? 'Error updating geometry:' : 'Error adding geometry:', error);
      addToast(isEditing ? 'Failed to update geometry' : 'Failed to add geometry', 'error');
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
    if (!selectedGeometryId) {
      addToast('Please select a geometry to delete.', 'info');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/geometries/${selectedGeometryId}/`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete geometry');
      }

      addToast('Geometry deleted successfully!', 'success');
      window.dispatchEvent(new CustomEvent('modelAdded'))
      resetForm();
      dispatch('geometryChanged');
      await loadGeometries();
    } catch (error) {
      console.error('Error deleting geometry:', error);
      addToast('Failed to delete geometry. Please try again.', 'error');
    }
  };

  // Ajout d'une fonction pour charger les détails d'une géométrie
  const loadGeometryDetails = async (id: string) => {
    try {
      const response = await fetch(`/api/geometries/${id}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch geometry details');
      }
      const geometry = await response.json();
      
      // Mise à jour des champs avec les valeurs de la géométrie sélectionnée
      name = geometry.name;
      type = geometry.type;
      color = geometry.color;
      position = { ...geometry.position };
      rotation = { ...geometry.rotation };
      isEditing = true;
      selectedGeometryId = id;
      
      console.log('Loaded geometry details:', geometry);
    } catch (error) {
      console.error('Error loading geometry details:', error);
      addToast('Failed to load geometry details', 'error');
    }
  };
</script>

<div class="form-container">
  <form on:submit|preventDefault={handleSubmit}>
    <h3>{isEditing ? 'Update' : 'Add'} Geometry</h3>
    
    <!-- Sélection de la géométrie -->
    <select 
      bind:value={selectedGeometryId} 
      on:change={handleGeometrySelect}
      class="geometry-select"
      style="width: auto;"
    >
      <option value="">Select a geometry to edit</option>
      {#each geometries as geometry}
        <option value={geometry.id}>{geometry.name} ({geometry.type})</option>
      {/each}
    </select>

    <input type="text" bind:value={name} placeholder="Name" required style="width: auto;" />
    <select bind:value={type} style="width: auto;">
      {#each types as geometryType}
        <option value={geometryType}>{geometryType}</option>
      {/each}
    </select>
    <input type="color" bind:value={color} style="width: auto;" />
    
    <div class="position-rotation">
      <div>
        <label for="position-x">Position:</label>
        <input id="position-x" type="number" bind:value={position.x} placeholder="X" step="0.01" style="width: auto;" /><br>
        <input id="position-y" type="number" bind:value={position.y} placeholder="Y" step="0.01" style="width: auto;" /><br>
        <input id="position-z" type="number" bind:value={position.z} placeholder="Z" step="0.01" style="width: auto;" />
      </div>
      <div>
        <label for="rotation-x">Rotation:</label>
        <input id="rotation-x" type="number" bind:value={rotation.x} placeholder="X" step="0.01" style="width: auto;" /><br>
        <input id="rotation-y" type="number" bind:value={rotation.y} placeholder="Y" step="0.01" style="width: auto;" /><br>
        <input id="rotation-z" type="number" bind:value={rotation.z} placeholder="Z" step="0.01" style="width: auto;" />
      </div>
    </div>

    <button 
      type="submit" 
      class={isEditing ? 'update-button' : 'add-button'}
    >
      {isEditing ? 'Update' : 'Add'} Geometry
    </button>
    {#if isEditing}
      <button 
        type="button" 
        on:click={resetForm} 
        class="cancel-button"
      >
        Cancel
      </button>
    {/if}
  </form>

  <div class="delete-section">
    <button 
      on:click={deleteGeometry} 
      disabled={!selectedGeometryId}
      class="delete-button"
    >
      Delete Selected Geometry
    </button>
  </div>
</div>

<style>
  .form-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 100%;
    margin: 0 auto;
    color: rgb(90, 115, 156);
    background-color: rgba(255, 255, 255, 0.9);
    padding: 0.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .geometry-select {
    margin-bottom: 1rem;
    padding: 0.5rem;
    width: 100%;
  }

  form, .delete-section {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  h3 {
    margin: 0.2rem 0;
    font-size: 1rem;
  }

  input, select, button {
    margin: 0.1rem 0;
    padding: 0.2rem;
    font-size: 0.9rem;
  }

  .position-rotation {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .position-rotation div {
    flex: 1;
  }

  .position-rotation label {
    display: block;
    margin-bottom: 0.2rem;
  }

  .position-rotation input {
    width: 100%;
    margin-bottom: 0.3rem;
  }

  .add-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .update-button {
    background-color: #ff9800;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .delete-button {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  @media (max-width: 600px) {
    .form-container {
      padding: 1rem;
    }

    .position-rotation {
      flex-direction: column;
    }

    input, select, button {
      font-size: 1rem;
      padding: 0.5rem;
    }
  }
</style>

