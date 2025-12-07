/**
 * 📥 Script de téléchargement en masse depuis Vercel Blob
 * 
 * Usage:
 *   1. Installer: npm install @vercel/blob
 *   2. Configurer BLOB_READ_WRITE_TOKEN dans .env
 *   3. Executer: node scripts/download-vercel-blob.js
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import { list } from '@vercel/blob';

// Configuration
const BLOB_READ_WRITE_TOKEN = process.env.BLOB_READ_WRITE_TOKEN || '';
const DOWNLOAD_DIR = './vercel-blob-backup';

if (!BLOB_READ_WRITE_TOKEN) {
    console.error('❌ Erreur: BLOB_READ_WRITE_TOKEN non défini');
    console.log('💡 Ajoutez-le dans .env ou passez-le en variable:');
    console.log('   BLOB_READ_WRITE_TOKEN=xxx node scripts/download-vercel-blob.js');
    process.exit(1);
}

async function downloadFile(url, filepath) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(filepath);

        https.get(url, (response) => {
            // Gestion redirections 302/307
            if (response.statusCode === 302 || response.statusCode === 307) {
                https.get(response.headers.location, (redirectResponse) => {
                    redirectResponse.pipe(file);
                    file.on('finish', () => {
                        file.close();
                        resolve();
                    });
                }).on('error', reject);
            } else if (response.statusCode === 200) {
                response.pipe(file);
                file.on('finish', () => {
                    file.close();
                    resolve();
                });
            } else {
                reject(new Error(`HTTP ${response.statusCode}: ${url}`));
            }
        }).on('error', (err) => {
            fs.unlink(filepath, () => { }); // Supprime fichier partiel
            reject(err);
        });
    });
}

async function downloadAllBlobs() {
    console.log('🚀 Début du téléchargement depuis Vercel Blob...\n');

    try {
        // Liste tous les fichiers
        const { blobs } = await list({
            token: BLOB_READ_WRITE_TOKEN,
            prefix: '', // tous les fichiers
        });

        console.log(`📦 ${blobs.length} fichiers trouvés\n`);

        // Créer le dossier de destination
        if (!fs.existsSync(DOWNLOAD_DIR)) {
            fs.mkdirSync(DOWNLOAD_DIR, { recursive: true });
        }

        // Sauvegarder la liste des fichiers
        const fileList = blobs.map(b => ({
            pathname: b.pathname,
            url: b.url,
            size: b.size,
            uploadedAt: b.uploadedAt
        }));

        fs.writeFileSync(
            path.join(DOWNLOAD_DIR, 'file-list.json'),
            JSON.stringify(fileList, null, 2)
        );
        console.log('✅ Liste des fichiers sauvegardée: file-list.json\n');

        // Télécharger chaque fichier
        let downloaded = 0;
        let errors = 0;

        for (const blob of blobs) {
            const filename = blob.pathname;
            const filepath = path.join(DOWNLOAD_DIR, filename);

            // Créer sous-dossiers si nécessaire
            const dir = path.dirname(filepath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }

            try {
                process.stdout.write(`⬇️  [${downloaded + 1}/${blobs.length}] ${filename}... `);
                await downloadFile(blob.url, filepath);
                console.log('✅');
                downloaded++;
            } catch (error) {
                console.log(`❌ Erreur: ${error.message}`);
                errors++;
            }
        }

        console.log(`\n${'='.repeat(50)}`);
        console.log(`✅ Téléchargement terminé !`);
        console.log(`   - Réussis: ${downloaded}/${blobs.length}`);
        console.log(`   - Erreurs: ${errors}`);
        console.log(`   - Dossier: ${DOWNLOAD_DIR}`);
        console.log(`${'='.repeat(50)}\n`);

    } catch (error) {
        console.error('❌ Erreur fatale:', error.message);
        process.exit(1);
    }
}

// Exécution
downloadAllBlobs();
