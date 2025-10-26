import * as THREE from 'three'
 
const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(70, window.innerWidth * 0.89 / window.innerHeight * 0.89)

const geometry = computeGeometry()
const material = new THREE.PointsMaterial( { size: 0.015, vertexColors: true } )
const mesh = new THREE.Points( geometry, material )

scene.add( mesh )

camera.position.set(0, 1, 2)
camera.lookAt(0, -0.5, 0)

const renderer = new THREE.WebGLRenderer({ canvas })

const clock = new THREE.Clock()
let t = 0

loop()


function loop() {
  t += clock.getDelta()
  animeGeometry(geometry, t)
  mesh.rotation.y = 0.1*t
  renderer.render(scene, camera)
  requestAnimationFrame(loop)
}

function computeGeometry() {

}



function animeGeometry(geometry, progress) {
  const space = 4, nb = 100, amp = 0.1, pi2= Math.PI*2
  const phase = progress
  const fre = 0.8 + Math.cos(progress)/2

  let k = 0
  for ( let i = 0; i < nb; i ++ ) {
    for ( let j = 0; j < nb; j ++ ) {
      const x = i*(space/nb)-space/2
      const z = j*(space/nb)-space/2
      const y = amp * ( Math.cos(x*pi2*fre+phase) + Math.sin(z*pi2*fre+phase) )
      geometry.attributes.position.setY(k, y)
      const intensity =( y/amp)/2+0.3
      geometry.attributes.color.setX(k, j/nb * intensity)
      geometry.attributes.color.setZ(k, i/nb * intensity)
      k ++
    }
  }
  geometry.attributes.position.needsUpdate = true
  geometry.attributes.color.needsUpdate = true 
}








