<script lang="ts">
  import * as THREE from 'three';
  import type { Scene, PerspectiveCamera } from 'three';
  
  export let scene: Scene;
  export let camera: PerspectiveCamera;
  
  const geometry = new THREE.BoxGeometry(1, 1, 1);
  const material = new THREE.MeshBasicMaterial({ color: 0x44ffff });
  const cube = new THREE.Mesh(geometry, material);
  
  scene.add(cube);
  
  // Add click event to the cube
  window.addEventListener('click', (event) => {
    const mouse = new THREE.Vector2(
      (event.clientX / window.innerWidth) * 2 - 1,
      -(event.clientY / window.innerHeight) * 2 + 1
    );
  
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
  
    const intersects = raycaster.intersectObject(cube);
    if (intersects.length > 0) {
      // Generate a random color
      const randomColor = Math.floor(Math.random() * 16777215);
      cube.material.color.setHex(randomColor);
    }
  });
  </script>