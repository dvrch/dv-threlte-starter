<script>
  import Block from './block.js';
  import { onMount } from 'svelte';
  import { Mesh } from 'three';
  import Rapier from '@dimforge/rapier3d-compat';
  // import App1 from '../svelte-demo-2N8/svelte-demo-main/src01/App.svelte';
  // import App2 from '../svelte-demo-2N8/svelte-demo-main/src02/App.svelte';
  // import App3 from '../svelte-demo-2N8/svelte-demo-main/src03/App.svelte';
  // import App4 from '../svelte-demo-2N8/svelte-demo-main/src04/App.svelte';
  // import App5 from '../svelte-demo-2N8/svelte-demo-main/src05/App.svelte';
  // import App6 from '../svelte-demo-2N8/svelte-demo-main/src06/App.svelte'
  // import App7 from '../svelte-demo-2N8/svelte-demo-main/src07/App.svelte';
  // import App8 from '../svelte-demo-2N8/svelte-demo-main/src08/App.svelte';
  // import App9 from '../svelte-demo-2N8/svelte-demo-main/src09/App.svelte';
  // import App10 from '../svelte-demo-2N8/svelte-demo-main/src10/App.svelte';
  // import App11 from '../svelte-demo-2N8/svelte-demo-main/src11/App.svelte';

  let block;
  onMount(async () => {
    await Rapier.init(); // Initialize Rapier
    const mesh = new Mesh(); // Remplacer par une instance réelle de Mesh
    const physic = new Rapier.World({ x: 0.0, y: -9.81, z: 0.0 }); // Pass gravity vector
    block = new Block(mesh, physic);
  });
</script>
 <!-- <App1 />
<App2 />
 <App3 /> 
<App4 />
<App5 />
<App6 />
<App7 />
<App8 />
<App9 />
<App10 /> -->