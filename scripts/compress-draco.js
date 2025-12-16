#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function compressGLB(inputPath, outputPath = null) {
    const filename = path.basename(inputPath);
    const dirname = path.dirname(inputPath);

    if (!outputPath) {
        const nameWithoutExt = path.basename(filename, '.glb');
        outputPath = path.join(dirname, `${nameWithoutExt}_draco.glb`);
    }

    console.log(`🔄 Compression de ${filename}...`);

    try {
        // Vérifier si gltf-transform est installé
        execSync('npx gltf-transform --version', { stdio: 'pipe' });

        // Commande de compression
        const cmd = `npx gltf-transform draco "${inputPath}" "${outputPath}"`;

        execSync(cmd, { stdio: 'inherit' });

        // Vérification des tailles
        const statsInput = fs.statSync(inputPath);
        const statsOutput = fs.statSync(outputPath);

        const originalSizeMB = statsInput.size / (1024 * 1024);
        const compressedSizeMB = statsOutput.size / (1024 * 1024);
        const ratio = ((1 - compressedSizeMB / originalSizeMB) * 100).toFixed(1);

        console.log(`✅ Compression réussie !`);
        console.log(`📊 Original: ${originalSizeMB.toFixed(2)} MB`);
        console.log(`📊 Compressé: ${compressedSizeMB.toFixed(2)} MB`);
        console.log(`📈 Ratio: ${ratio}%`);

        return outputPath;

    } catch (error) {
        console.error(`❌ Erreur lors de la compression: ${error.message}`);
        console.log('\n📦 Installation des dépendances requises:');
        console.log('npm install -g @gltf-transform/cli');
        return null;
    }
}

async function compressFolder(folderPath) {
    const files = fs.readdirSync(folderPath);
    const glbFiles = files.filter(f => f.endsWith('.glb') && !f.includes('_draco'));

    console.log(`📁 Dossier: ${folderPath}`);
    console.log(`📦 ${glbFiles.length} fichiers GLB à compresser\n`);

    for (const file of glbFiles) {
        const inputPath = path.join(folderPath, file);
        await compressGLB(inputPath);
        console.log('─'.repeat(50));
    }
}

// Interface en ligne de commande
const args = process.argv.slice(2);

if (args.length === 0) {
    // Mode dossier par défaut
    compressFolder('./static/public/');
} else if (args[0] === '--folder' && args[1]) {
    // Spécifier un dossier
    compressFolder(args[1]);
} else if (args[0] === '--file' && args[1]) {
    // Compresser un fichier spécifique
    const outputFile = args[2] || null;
    compressGLB(args[1], outputFile);
} else {
    console.log('Usage:');
    console.log('  node compress-draco.js                    # Compresser tout le dossier public');
    console.log('  node compress-draco.js --folder <path>   # Spécifier un dossier');
    console.log('  node compress-draco.js --file <input> [output] # Compresser un fichier');
}
