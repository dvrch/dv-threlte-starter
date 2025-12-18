<script lang="ts">
  import * as THREE from 'three';
  import { onMount } from 'svelte';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
  
  let scene: THREE.Scene;
  let camera: THREE.PerspectiveCamera;
  let renderer: THREE.WebGLRenderer;
  let cube: THREE.Mesh<THREE.BoxGeometry, THREE.MeshBasicMaterial>;
  let controls: OrbitControls;
  
  onMount(() => {
    renderer = new THREE.WebGLRenderer({
      canvas: document.getElementById('canvas') as HTMLCanvasElement,
      antialias: true
    });
  
    // Initialize the scene
    scene = new THREE.Scene();
  
    // Initialize the camera
    camera = new THREE.PerspectiveCamera(75, 500 / 500, 0.1, 1000);
    camera.position.z = 5;
  
    // Initialize OrbitControls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableZoom = true;
  
    // Create the cube
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x44ffff });
    cube = new THREE.Mesh(geometry, material);
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
  
    // Animate the scene
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  });
  </script>
  
  <canvas id="canvas" width="500" height="500"></canvas>