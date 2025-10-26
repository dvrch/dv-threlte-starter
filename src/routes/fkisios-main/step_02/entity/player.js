import { Object3D, Vector3 } from 'three'
import Gamepad from '../control/gamepad'
import { createRigidBodyEntity, range } from '../tool/function'

const SPEED = 3

export default class Player extends Object3D {
  collider = null
  rigidBody = null
  animator = null
  ctrl = new Gamepad()

  constructor(mesh, physic) {
    super()
    const origin = new Vector3(0, 4, 0)
    this.initPhysic(physic, origin)
    this.initVisual(mesh)
  }

  initPhysic(physic, origin) {
    const { rigidBody, collider } = createRigidBodyEntity(origin, physic)
    this.rigidBody = rigidBody
    this.collider = collider
  }

  initVisual(mesh) {
    this.add(mesh)
  }

  update(dt) {
    this.updatePhysic()
    this.updateVisual(dt)
  }

  updatePhysic() {
    let x = this.ctrl.x * SPEED
    let z = this.ctrl.z * SPEED
    let y = this.rigidBody.linvel().y
    this.rigidBody.setLinvel({ x, y, z }, true)
  }

  updateVisual(dt) {
    this.position.copy(this.rigidBody.translation())
    if(this.ctrl.moving) {
      this.rotation.y += range(this.ctrl.angle, this.rotation.y) * dt * 10
    }
  }
}
