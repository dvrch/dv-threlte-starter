import sqlite3 from 'sqlite3';
import fs from 'fs';
import path from 'path';

const STATIC_DIR = path.join(process.cwd(), 'static/data');
const DB_FILE = path.join(STATIC_DIR, 'inventory.sqlite');

/**
 * 🛠️ Script de synchronisation REVERSE: SQLite -> JSON
 * permet de travailler directement dans un gestionnaire de BD externe 
 * et de mettre à jour l'application d'un coup.
 */
function refreshFromJson() {
    console.log(`🏗️ Reading from SQLite DB: ${DB_FILE}...`);

    if (!fs.existsSync(DB_FILE)) {
        console.error("❌ Database file not found!");
        return;
    }

    const db = new sqlite3.Database(DB_FILE);

    // 1. Sync Types
    db.all("SELECT id FROM types", [], (err, rows) => {
        if (err) {
            console.error("❌ Error reading types:", err.message);
            return;
        }
        const types = rows.map(r => ({ id: r.id, name: r.id }));
        fs.writeFileSync(path.join(STATIC_DIR, 'types.json'), JSON.stringify(types, null, 2));
        console.log(`✅ types.json updated (${types.length} types)`);
    });

    // 2. Sync Geometries
    db.all("SELECT * FROM geometries", [], (err, rows) => {
        if (err) {
            console.error("❌ Error reading geometries:", err.message);
            return;
        }

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

        db.close();
    });
}

refreshFromJson();
