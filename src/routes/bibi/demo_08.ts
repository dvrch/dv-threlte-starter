import * as THREE from 'three'
import GLTFLoader from 'gltfloader'
import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets'

const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.89 / window.innerHeight * 0.89)

// const mesh = await GLTFLoader.loadObject('cloth_sim.glb', 'cloth')
const mesh = await GLTFLoader.loadObject(getCloudinaryAssetUrl('bibi3.glb'), 'bibi')
const texture = new THREE.TextureLoader().load(getCloudinaryAssetUrl('bibi.png'))
mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 0 })

const light = new THREE.PointLight(0xeeeeee)

scene.add(light)
scene.add(mesh)

camera.position.set(0, 1.5, 4)
light.position.set(0, 4, 4)

const renderer = new THREE.WebGLRenderer({ canvas })

const mixer = new THREE.AnimationMixer(mesh)
mixer.clipAction(mesh.animations[0]).setDuration(4).play()
const clock = new THREE.Clock()

loop()

function loop() {
  requestAnimationFrame(loop)
  const dt = clock.getDelta()
  mixer.update(dt)
  renderer.render(scene, camera)
}