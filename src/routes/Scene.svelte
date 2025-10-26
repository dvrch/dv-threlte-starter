<script>
  // ... autres imports existants ...
  import { BloomEffect, EffectComposer, EffectPass, KernelSize, RenderPass, SMAAEffect, SMAAPreset } from 'postprocessing'
  
  const { scene, renderer, camera } = useThrelte()
  const composer = new EffectComposer(renderer)
  composer.setSize(innerWidth, innerHeight)

  const setupEffectComposer = () => {
    composer.removeAllPasses()
    composer.addPass(new RenderPass(scene, camera.current))
    composer.addPass(
      new EffectPass(
        camera.current,
        new BloomEffect({
          intensity: 0.8,
          luminanceThreshold: 0,
          height: 512, 
          width: 512,
          luminanceSmoothing: 0,
          mipmapBlur: true,
          kernelSize: KernelSize.MEDIUM
        })
      )
    )
    composer.addPass(
      new EffectPass(
        camera.current,
        new SMAAEffect({
          preset: SMAAPreset.LOW
        })
      )
    )
  }

  $: if ($camera) setupEffectComposer($camera)

  useRender((_, delta) => {
    // Mettre à jour l'environnement et le rendu
    setupEnvironmentMapping()
    composer.render(delta)
  })

  onMount(() => {
    setupEffectComposer()
    setupEnvironmentMapping()
    
    const interval = setInterval(() => {
      setupEnvironmentMapping()
    }, 1000)
    
    cleanupFunctions.push(() => {
      clearInterval(interval)
      composer.dispose()
    })
  })
</script>

<div class="div">
  <T.PerspectiveCamera makeDefault position={[-5, 6, 10]} fov={25}>
    <OrbitControls enableDamping target={[0, 0, 0]} />
  </T.PerspectiveCamera>
  
  <T.DirectionalLight intensity={1.8} position={[0, 10, 0]} castShadow shadow.bias={-0.0001} />

  <Spaceship
    bind:ref={spaceShipRef}
    position={[0, translY, 0]}
    rotation={[angleZ, 0, angleZ, 'ZXY']}
  />

  <Vague 
    bind:ref={spaceShipRef}
    position={[0, translY, 0]}
    scale={6}
  />
  
  <Stars />
  
  <Nissan
    bind:ref={spaceShipRef}
    position={[0, translY, 0]}
    rotation={[angleZ, 80, angleZ, 'ZXY']}
  />
</div> 