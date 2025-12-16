import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'

export function createDracoLoader() {
    const dracoLoader = new DRACOLoader()
    dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/')
    dracoLoader.setDecoderConfig({ type: 'js' })
    return dracoLoader
}

export function setupDracoLoader(loader) {
    const dracoLoader = createDracoLoader()
    loader.setDRACOLoader(dracoLoader)

    return loader
}
