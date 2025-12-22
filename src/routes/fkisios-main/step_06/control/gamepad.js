import { floor } from '../tool/function'

const ATTACK = 0
const JUMP = 1
const LOCK = 7
const X = 0
const Z = 1

export default class Gamepad {
  keys = {}

  constructor() {
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', (e) => this.keys[e.code] = true)
      window.addEventListener('keyup', (e) => this.keys[e.code] = false)
    }
  }

  get gamepad() {
    return typeof navigator !== 'undefined' && navigator.getGamepads ? navigator.getGamepads()[0] : null
  }

  get x() {
    // Keyboard support (WASD / Arrows)
    let kX = 0
    if (this.keys['KeyD'] || this.keys['ArrowRight']) kX += 1
    if (this.keys['KeyA'] || this.keys['ArrowLeft']) kX -= 1

    if (kX !== 0) return kX

    if (!this.gamepad) return 0
    return floor(this.gamepad.axes[X])
  }

  get z() {
    // Keyboard support (WASD / Arrows)
    let kZ = 0
    if (this.keys['KeyS'] || this.keys['ArrowDown']) kZ += 1
    if (this.keys['KeyW'] || this.keys['ArrowUp'] || this.keys['KeyZ']) kZ -= 1

    if (kZ !== 0) return kZ

    if (!this.gamepad) return 0
    return floor(this.gamepad.axes[Z])
  }

  get attack() {
    if (this.keys['Space'] || this.keys['KeyE']) return true
    if (!this.gamepad) return false
    return this.gamepad.buttons[ATTACK]?.pressed
  }

  get jump() {
    if (this.keys['Space']) return true
    if (!this.gamepad) return false
    return this.gamepad.buttons[JUMP]?.pressed
  }

  get lock() {
    if (this.keys['ShiftLeft'] || this.keys['KeyQ']) return true
    if (!this.gamepad) return false
    return this.gamepad.buttons[LOCK]?.pressed
  }

  get moving() {
    return Math.abs(this.x) || Math.abs(this.z)
  }

  get angle() {
    return Math.atan2(-this.z, this.x) + Math.PI / 2
  }
}
