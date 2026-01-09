import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const STATIC_DIR = path.join(process.cwd(), 'static/data');
const DB_FILE = path.join(STATIC_DIR, 'inventory.sqlite');

/**
 * 🏗️ Script de synchronisation REVERSE: SQLite -> JSON
 * Utilise l'outil ligne de commande 'sqlite3' pour éviter les erreurs de bindings Node.
 */
function refreshFromJson() {
    console.log(`🏗️ Reading from SQLite DB via CLI: ${DB_FILE}...`);

    if (!fs.existsSync(DB_FILE)) {
        console.error("❌ Database file not found at " + DB_FILE);
        return;
    }

    try {
        // 1. Sync Types
        const typesRaw = execSync(`sqlite3 ${DB_FILE} -json "SELECT id FROM types"`).toString();
        const types = JSON.parse(typesRaw || '[]').map(r => ({ id: r.id, name: r.id }));
        fs.writeFileSync(path.join(STATIC_DIR, 'types.json'), JSON.stringify(types, null, 2));
        console.log(`✅ types.json updated (${types.length} types)`);

        // 2. Sync Geometries
        const geoRaw = execSync(`sqlite3 ${DB_FILE} -json "SELECT * FROM geometries"`).toString();
        const rows = JSON.parse(geoRaw || '[]');

        const geometries = rows.map(row => ({
            id: row.id,
            name: row.name,
            type: row.type,
            color: row.color,
            position: { x: row.position_x, y: row.position_y, z: row.position_z },
            rotation: { x: row.rotation_x, y: row.rotation_y, z: row.rotation_z },
            scale: { x: row.scale_x, y: row.scale_y, z: row.scale_z },
            visible: row.visible === 1,
            model_url: row.model_url
        }));

        fs.writeFileSync(path.join(STATIC_DIR, 'geometries.json'), JSON.stringify(geometries, null, 2));
        console.log(`✅ geometries.json updated (${geometries.length} objects)`);

    } catch (error) {
        console.error("❌ Extraction failed. Make sure 'sqlite3' is installed on your system.");
        console.error(error.message);
    }
}

refreshFromJson();
