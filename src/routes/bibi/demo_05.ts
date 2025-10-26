import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

export async function initScene(canvas: HTMLCanvasElement){
const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.89 / window.innerHeight * 0.89)


// const geometry = await GLTFLoader.loadGeometry('/public/cloth_sim.glb', '/public/cloth')
// const geometry = await GLTFLoader.loadGeometry('/public/bibi2.glb')
// const geometry = await GLTFLoader.loadGeometry('/public/Barrel Model1.glb')


const loader = new GLTFLoader()
const gltf = await loader.loadAsync('/public/Barrel Model1.glb') //('/public/mario.glb')
const geometry = (gltf.scene.children[0] as THREE.Mesh).geometry
// const geometry = firstChild instanceof THREE.Mesh ? firstChild.geometry : new THREE.BufferGeometry()

const texture = new THREE.TextureLoader().load('/public/mario.png')
// const texture = new THREE.TextureLoader().load('/public/Tout.jpg', '/public/mario.png')


const material = new THREE.MeshPhongMaterial({ map:texture,shininess:0})

const mesh = new THREE.Mesh(geometry, material)

const light = new THREE.PointLight(0xeeeeee)
const alight = new THREE.AmbientLight(0x555555)
const directionalLight = new THREE.DirectionalLight(0xffffff, 1) // Ajouter une lumière directionnelle
directionalLight.position.set(0, 1, 1).normalize()
scene.add(directionalLight)
// ... code existant ...

scene.add(light)
scene.add(alight)
scene.add(directionalLight)
scene.add(mesh)

camera.position.set(0, 1.5, 4)
light.position.set(0, 4, 4)

const renderer = new THREE.WebGLRenderer({ canvas })
renderer.setSize(window.innerWidth * 0.89, window.innerHeight * 0.89)

// Supprimez cette fonction si elle n'est pas nécessaire
const onLoad = () => {
    // votre code ici
};

loop()

function loop() {
  requestAnimationFrame(loop)
  mesh.rotation.y += 0.01
  renderer.render(scene, camera)
}
}
