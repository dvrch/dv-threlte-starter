import * as THREE from 'three'
import GLTFLoader from 'gltfloader'
import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';
 
const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.89 / window.innerHeight * 0.89)

// const geometry = await GLTFLoader.loadGeometry('ALIMIC 20.glb')

const geometry = await GLTFLoader.loadGeometry(getCloudinaryAssetUrl('mario.glb'))
const texture = await GLTFLoader.loadTexture('mario.png')
const material = new THREE.MeshPhongMaterial({ map:texture,shininess:1 })

const mesh = new THREE.Mesh(geometry, material)

const light = new THREE.PointLight(0xffffff)

scene.add(light)
scene.add(mesh)

camera.position.set(0, 1.5, 4)
light.position.set(0, 4, 4)

const renderer = new THREE.WebGLRenderer({ canvas })

let t = 0
const clock = new THREE.Clock();

loop()

function loop() {
  t += clock.getDelta()
  mesh.morphTargetInfluences[1] = Math.abs(Math.cos(t))
  mesh.rotation.y = Math.cos(t/2)
  renderer.render(scene, camera)
  requestAnimationFrame(loop)
}
