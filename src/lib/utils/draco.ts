import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { useLoader } from '@threlte/core';

// Crée une instance de DRACOLoader mise en cache globalement
export const dracoLoader = useLoader(DRACOLoader, {
  extend: (loader) => {
    loader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
  }
});
