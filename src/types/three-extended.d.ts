// src/types/three-extended.d.ts
declare module "three/examples/jsm/geometries/TextGeometry" {
  import { BufferGeometry } from "three";
  import { Font } from "three/examples/jsm/loaders/FontLoader";

  export class TextGeometry extends BufferGeometry {
    constructor(
      text: string,
      parameters: {
        font: Font;
        size?: number;
        height?: number;
        curveSegments?: number;
        bevelEnabled?: boolean;
        bevelThickness?: number;
        bevelSize?: number;
        bevelOffset?: number;
        bevelSegments?: number;
      }
    );
  }
}
