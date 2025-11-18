import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";
import * as THREE from "three";
import { getAssetUrl } from "$lib/asset-helper";

const scene = new THREE.Scene(); // Add this line to define the scene

const loader = new FontLoader();
loader.load(getAssetUrl("/fonts/HK.ttf"), (font) => {
  const geometry = new TextGeometry("Sample Text", {
    font: font,
    size: 1,
    height: 0.1,
  });
  const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});
