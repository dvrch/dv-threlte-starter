<script>
  import { onMount } from 'svelte';
  import { Scene } from 'three';
  import Camera from './engine/camera';
  import Light from './engine/light';
  import Graphic from './engine/graphic';
  import World from './entity/world';
  import Player from './entity/player';
  import { loadWorld, loadEntity } from './tool/loader';
  import physic from './engine/physic';

  let scene: Scene;
  let camera: Camera;
  let world: World;
  let player: Player;
  let light: Light;
  let graphic: Graphic;

  onMount(async () => {
    const assetW = await loadWorld('./glb/world2.glb');
    const assetP = await loadEntity('./glb/character.glb');

    scene = new Scene();
    camera = new Camera();
    world = new World(assetW.visuals, assetW.colliders, physic, assetW.areas);
    player = new Player(assetP, physic);
    light = new Light();

    scene.add(world);
    scene.add(light);
    scene.add(player);

    graphic = new Graphic(scene, camera);
    graphic.onUpdate((dt: number) => {
      physic.step();
      player.update(dt, world.areas);
      camera.update(player);
      light.update(player);
    });
  });
</script>
