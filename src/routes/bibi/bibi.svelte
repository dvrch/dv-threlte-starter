<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { initSn } from './demo_09.js';
	import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
	import * as THREE from 'three';
	import { AssetManager } from '$lib/config';

	let { width = 100, height = 100 } = $props();

	let canvas: HTMLCanvasElement;
	let animationId: number;
	let controls: OrbitControls;

	const dispatch = createEventDispatcher();

	onMount(() => {
		let cleanup: (() => void) | undefined;

		if (canvas) {
			initSn(canvas)
				.then(({ renderer, scene, camera, animate }) => {
					if (camera) {
						controls = new OrbitControls(camera, renderer.domElement);

						function loop() {
							scene.rotation.y += 0.01;
							animate();
							controls.update();
							renderer.render(scene, camera);
							dispatch('render', { scene, camera, renderer });
							animationId = requestAnimationFrame(loop);
						}

						loop();

						cleanup = () => {
							cancelAnimationFrame(animationId);
							renderer.dispose();
							controls.dispose();
						};

						dispatch('sceneInitialized', { scene, camera, renderer, controls });
					} else {
						console.error("La caméra n'est pas définie.");
					}
				})
				.catch((error) => {
					console.error("Erreur lors de l'initialisation de la scène:", error);
				});
		}

		return () => {
			cleanup?.();
		};
	});
</script>

<canvas bind:this={canvas} {width} {height} />

<!--
<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { T, Canvas } from '@threlte/core';
  import { Grid, OrbitControls, TransformControls } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { OrbitControls as ThreeOrbitControls } from 'three/examples/jsm/controls/OrbitControls';

  let { width = 100 } = $props();
  let { height = 100 } = $props();

  let canvas: HTMLCanvasElement;
  let animationId: number;
  let controls: ThreeOrbitControls;
  let bibiScene: THREE.Scene;
  let bibiCamera: THREE.Camera;
  let bibiRenderer: THREE.WebGLRenderer;
  let mixer: THREE.AnimationMixer;

  const dispatch = createEventDispatcher();

  async function initScene(canvas: HTMLCanvasElement) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    camera.position.set(0, 1.5, 5.2);

    let gltf = await new GLTFLoader().loadAsync(AssetManager.getAssetUrl('public/cloth_sim.glb'));
    const mesh = gltf.scene.children[0] as THREE.Mesh;
    
    let texture = await new THREE.TextureLoader().loadAsync(AssetManager.getAssetUrl('public/bibi.png'));
    
    if (mesh.material) {
      mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
    }

    mixer = new THREE.AnimationMixer(mesh);
    if (gltf.animations && gltf.animations.length > 0) {
      gltf.animations.forEach((clip) => {
        mixer.clipAction(clip).play();
      });
      console.log(`Nombre d'animations trouvées: ${gltf.animations.length}`);
    } else {
      console.warn("Aucune animation trouvée dans le modèle GLTF.");
    }

    const light = new THREE.PointLight(0xFFFFFF);
    const alight = new THREE.AmbientLight(0x555555, 10);

    light.position.set(0, 4, 4);

    scene.add(light);
    scene.add(mesh);
    scene.add(alight);

    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(window.innerWidth * 0.89, window.innerHeight * 0.89);
    renderer.setClearColor(0x000000, 0);

    return { renderer, scene, camera, mesh };
  }

  onMount(() => {
    let cleanup: (() => void) | undefined;
    const clock = new THREE.Clock();

    if (canvas) {
      initScene(canvas).then(({ renderer, scene, camera, mesh }) => {
        bibiScene = scene;
        bibiCamera = camera;
        bibiRenderer = renderer;
        
        if (camera) {
          controls = new ThreeOrbitControls(camera, renderer.domElement);

          function loop() {
            const dt = clock.getDelta();
            mixer.update(dt);
            mesh.rotation.y += dt;
            scene.rotation.y += 0.01;
            controls.update();
            renderer.render(scene, camera);
            dispatch('render', { scene, camera, renderer });
            animationId = requestAnimationFrame(loop);
          }
          
          loop();
          
          cleanup = () => {
            cancelAnimationFrame(animationId);
            renderer.dispose();
            controls.dispose();
          };

          dispatch('sceneInitialized', { scene, camera, renderer, controls });
        }
      }).catch(error => {
        console.error("Erreur lors de l'initialisation de la scène:", error);
      });
    }

    return () => {
      cleanup?.();
    };
  });
</script>

<div class="scene-container">
  <Canvas>
    <T.PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>

    <T.Scene>
      {#if bibiScene}
        <T is={bibiScene} />
      {/if} 
    </T.Scene>
  </Canvas>

  <div class="bibi-container">
    <canvas bind:this={canvas} {width} {height}></canvas>
  </div>
</div>

<style>
  .scene-container {
    position: relative;
    width: 100%;
    height: 100vh;
  }

  .bibi-container {
    position: absolute;
    bottom: 20px;
    right: 20px;
    width: 400px;
    height: 300px;
  }

  canvas {
    width: 100%;
    height: 100%;
  }
</style>
-->

<style>
	canvas {
		width: 100%;
		height: 100%;
	}
</style>
