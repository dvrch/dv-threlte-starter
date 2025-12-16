// remove-morphs.mjs
import { NodeIO } from '@gltf-transform/core';
import { prune } from '@gltf-transform/functions';
import { KHRONOS_EXTENSIONS, EXTTextureWebP } from '@gltf-transform/extensions';
import draco3d from 'draco3dgltf';

async function main() {
    const io = new NodeIO()
        .registerExtensions([...KHRONOS_EXTENSIONS, EXTTextureWebP])
        .registerDependencies({
            'draco3d.decoder': await draco3d.createDecoderModule(),
            'draco3d.encoder': await draco3d.createEncoderModule(),
        });

    const inputPath = process.argv[2];
    const outputPath = process.argv[3];

    if (!inputPath || !outputPath) {
      console.error('Usage: node remove-morphs.mjs <input.glb> <output.glb>');
      process.exit(1);
    }

    console.log(`Reading input file: ${inputPath}`);
    const document = await io.read(inputPath);
    const root = document.getRoot();

    let totalTargetsRemoved = 0;

    // Iterate through all meshes and remove morph targets
    for (const mesh of root.listMeshes()) {
      for (const prim of mesh.listPrimitives()) {
        const targets = prim.listTargets();
        if (targets.length > 0) {
          console.log(`Removing ${targets.length} morph targets from mesh '${mesh.getName()}'.`);
          totalTargetsRemoved += targets.length;
          prim.listTargets().forEach(target => target.dispose());
        }
      }
    }

    if (totalTargetsRemoved > 0) {
        console.log(`Total morph targets removed: ${totalTargetsRemoved}. Pruning unused data...`);
        // Prune unreferenced data after removing morph targets
        await document.transform(prune());
    } else {
        console.log('No morph targets found to remove.');
    }


    await io.write(outputPath, document);

    console.log(`Successfully processed file and wrote to ${outputPath}`);
}

main().catch((e) => {
    console.error(e);
    process.exit(1);
});