<script lang="ts">
import { onMount } from 'svelte';
import * as THREE from 'three';

let canvas: HTMLCanvasElement;

onMount(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const mesh = new THREE.Mesh(geometry, material);
    
    scene.add(mesh);
    camera.position.set(0, 0, 2);
    
    const canvas = document.createElement('canvas');
    document.body.appendChild(canvas);
    const renderer = new THREE.WebGLRenderer({ canvas });
    
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    
    animate(); // Démarre l'animation
});
</script>


<div class="div">
  <canvas bind:this={canvas} id="canvas"></canvas>
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
		/* transition: transform 0.5s ease;  */
	}
</style>
