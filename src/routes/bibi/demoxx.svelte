
<script lang="ts">
import { onMount } from 'svelte';
import * as THREE from 'three';

let canvas: HTMLCanvasElement;

onMount(() => {
  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.89 / window.innerHeight * 0.89);

  const geometry = new THREE.BoxGeometry(1, 1, 1);

  const texture = new THREE.TextureLoader().load('/src/routes/bibi/diamond.jpg');
  const material = new THREE.MeshPhongMaterial({ map: texture });

  const mesh = new THREE.Mesh(geometry, material);

  const light = new THREE.PointLight(0xeeeeee);

  scene.add(light);
  scene.add(mesh);

  camera.position.set(0, 0, 3);
  light.position.set(0, 0, 3);

  const renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(window.innerWidth * 0.8, window.innerHeight * 0.8);

  loop();

  function loop() {
    requestAnimationFrame(loop);
    mesh.rotation.x += 0.005;
    mesh.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
});
</script> 
<canvas bind:this={canvas} id="canvas"></canvas>