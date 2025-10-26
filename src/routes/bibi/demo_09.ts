import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
 
export async function initSn(canvas: HTMLCanvasElement){

const scene = new THREE.Scene()

// Créer et positionner la caméra
const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
camera.position.set(0, 1.5, 5.2); // Positionner la caméra

let gltf;
try {
  gltf = await new GLTFLoader().loadAsync('/public/cloth_sim.glb');
} catch (error) {
  console.error("Erreur lors du chargement du modèle GLTF:", error);
  throw error; // Propager l'erreur
}

const mesh = gltf.scene.children[0] as THREE.Mesh; // Accéder au mesh
let texture;
try {
  texture = await new THREE.TextureLoader().loadAsync('/public/bibi.png');
} catch (error) {
  console.error("Erreur lors du chargement de la texture:", error);
  throw error; // Propager l'erreur
}

if (mesh.material) {
  mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
}

const light = new THREE.PointLight(0xFFFFFF)
const alight = new THREE.AmbientLight(0x555555, 10)

scene.add(light)
scene.add(mesh)
scene.add(alight)

const renderer = new THREE.WebGLRenderer({ canvas })
renderer.setSize(window.innerWidth * 0.89, window.innerHeight * 0.89)
renderer.setClearColor(0x000000, 0); // Définir l'arrière-plan comme transparent

camera.position.set(0, 1.5, 5.2)
light.position.set(0, 4, 4)

const mixer = new THREE.AnimationMixer(mesh);

if (gltf.animations && gltf.animations.length > 0) {
  gltf.animations.forEach((clip) => {
    mixer.clipAction(clip).play();
  });
  console.log(`Nombre d'animations trouvées: ${gltf.animations.length}`);
} else {
  console.warn("Aucune animation trouvée dans le modèle GLTF.");
}

const clock = new THREE.Clock();
function animate() {
  const dt = clock.getDelta();
  mixer.update(dt);
  mesh.rotation.y += dt; // Rotation continue
  renderer.render(scene, camera);
}

// return { renderer, animate };
return Promise.resolve({ renderer, scene, camera, animate });
}
