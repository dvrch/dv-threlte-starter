
import { put } from '@vercel/blob';
import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';

// Load env variables
dotenv.config({ path: 'backend/.env' });

const token = process.env.BLOB_READ_WRITE_TOKEN;

if (!token) {
    console.error("❌ Error: BLOB_READ_WRITE_TOKEN not found in backend/.env");
    process.exit(1);
}

const FILES_TO_UPLOAD = [
    "static/public/cloth_sim.glb",
    "static/public/DRAP+Barrel Model1.glb",
    "static/assets/Desk-bati.glb",
    "static/models/spaceship.glb",
    "static/models/nissan1.glb",
    "static/public/nissan2.glb",
    "static/models/nissan.glb",
    "static/assets/nissan.glb"
];

async function uploadFile(filePath) {
    if (!fs.existsSync(filePath)) {
        console.warn(`⚠️ File not found: ${filePath} (Skipping)`);
        return null;
    }

    const filename = path.basename(filePath);
    const pathname = `static-assets/${filename}`;

    console.log(`📤 Uploading ${filename}...`);

    try {
        const fileContent = fs.readFileSync(filePath);
        const blob = await put(pathname, fileContent, {
            access: 'public',
            token: token
        });

        console.log(`✅ Uploaded: ${blob.url}`);
        return { localPath: filePath, url: blob.url };
    } catch (error) {
        console.error(`❌ Failed to upload ${filePath}:`, error);
        return null;
    }
}

async function main() {
    const results = {};

    for (const filePath of FILES_TO_UPLOAD) {
        const res = await uploadFile(filePath);
        if (res) {
            results[res.localPath] = res.url;
        }
    }

    console.log("\n--- SUMMARY OF UPLOADS ---");
    console.log(JSON.stringify(results, null, 2));
}

main().catch(console.error);
