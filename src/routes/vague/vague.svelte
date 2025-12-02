<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import * as THREE from 'three';
  // import Bibi from './../bibi/+page.svelte';

  let { width = createEventDispatcher() }: { width?: 100;
  export let height: 100;

  let canvas: HTMLCanvasElement;
  const dispatch } = $props();

  onMount(() => {
    const scene = new THREE.Scene();
    // const camera = new THREE.PerspectiveCamera(70, canvas.offsetWidth / canvas.offsetHeight);
    const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.85 / window.innerHeight * 0.85);
    const geometry = computeGeometry();
    const material = new THREE.PointsMaterial({ size: 0.015, vertexColors: true });
    const mesh = new THREE.Points(geometry, material);

    scene.add(mesh);

    camera.position.set(0, 1, 2);
    camera.lookAt(0, -0.5, 0);

    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(window.innerWidth, window.innerHeight); // Ajout de cette ligne
    renderer.setSize(canvas.offsetWidth , canvas.offsetHeight); 
    renderer.setClearColor(0x000000, 1); // Ajout de cette ligne pour définir la couleur de fond

    const clock = new THREE.Clock();
    let t = 0;

    loop();

    function loop() {
      t += clock.getDelta();
      animeGeometry(geometry, t);
      mesh.rotation.y = 0.1 * t;
      renderer.render(scene, camera);
      dispatch('render', { scene, camera, renderer });
      requestAnimationFrame(loop);
    }

    function computeGeometry(): THREE.BufferGeometry {
      const space = 4, nb = 100, amp = 0.1, pi2 = Math.PI * 2;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(nb * nb * 3);
      const colors = new Float32Array(nb * nb * 3);
      let k = 0;

      for (let i = 0; i < nb; i++) {
        for (let j = 0; j < nb; j++) {
          const x = i * (space / nb) - space / 2;
          const z = j * (space / nb) - space / 2;
          const y = amp * (Math.cos(x * pi2) + Math.sin(z * pi2));
          positions[3 * k + 0] = x;
          positions[3 * k + 1] = y;
          positions[3 * k + 2] = z;
          const intensity = (y / amp) / 2 + 0.3;
          colors[3 * k + 0] = j / nb * intensity;
          colors[3 * k + 1] = 0;
          colors[3 * k + 2] = i / nb * intensity;
          k++;
        }
      }
      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
      geometry.computeBoundingBox();
      return geometry;
    }

    function animeGeometry(geometry: THREE.BufferGeometry, progress: number): void {
      const space = 4, nb = 100, amp = 0.1, pi2 = Math.PI * 2;
      const phase = progress;
      const fre = 0.8 + Math.cos(progress) / 2;

      let k = 0;
      for (let i = 0; i < nb; i++) {
        for (let j = 0; j < nb; j++) {
          const x = i * (space / nb) - space / 2;
          const z = j * (space / nb) - space / 2;
          const y = amp * (Math.cos(x * pi2 * fre + phase) + Math.sin(z * pi2 * fre + phase));
          geometry.attributes.position.setY(k, y);
          const intensity = (y / amp) / 2 + 0.3;
          geometry.attributes.color.setX(k, j / nb * intensity);
          geometry.attributes.color.setZ(k, i / nb * intensity);
          k++;
        }
      }
      geometry.attributes.position.needsUpdate = true;
      geometry.attributes.color.needsUpdate = true;
    }

    // Ajout de cette ligne pour gérer le démontage
    return () => {
      // Nettoyage si nécessaire
      renderer.dispose(); // Libération des ressources du renderer
    };
  });
</script>
<div class="div">
  <canvas bind:this={canvas} {width} {height}></canvas>
</div>

<style>
* {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
.div {position: absolute; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  z-index: -2;
  transform: scale(1.2);
  transition: transform 0.5s ease;
}
canvas {
  width: 100%;
  height: 100%;
}
</style>
