<script>
  import { onMount } from 'svelte';
  import { BloomEffect, EffectComposer, EffectPass, KernelSize, RenderPass, SMAAEffect, SMAAPreset } from 'postprocessing'
  
  import { useThrelte, useTask } from '@threlte/core'

  const { renderer, scene, camera } = useThrelte(); // Get renderer, scene, and camera from useThrelte

  let composer; // Declare composer here

  const setupEffectComposer = () => {
    if (!renderer || !scene || !camera.current) return; // Ensure they are defined

    if (!composer) { // Initialize composer only once
      composer = new EffectComposer(renderer);
      composer.setSize(window.innerWidth, window.innerHeight);
    }

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


  useTask((_, delta) => {
    // Mettre à jour l'environnement et le rendu
    setupEnvironmentMapping() // Assuming this function is defined elsewhere
    if (composer) { // Only render if composer is initialized
      composer.render(delta)
    }
  })

  onMount(() => {
    setupEffectComposer()
    setupEnvironmentMapping() // Assuming this function is defined elsewhere
    
    const interval = setInterval(() => {
      setupEnvironmentMapping()
    }, 1000)
    
    // Assuming cleanupFunctions is defined elsewhere
    cleanupFunctions.push(() => {
      clearInterval(interval)
      if (composer) {
        composer.dispose()
      }
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