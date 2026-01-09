import fs from 'fs';
import { execSync } from 'child_process';
import path from 'path';

const JSON_FILE = 'static/data/sv-dv-scene-2026-01-09.json';
const DB_FILE = 'static/data/inventory.sqlite';

if (!fs.existsSync(JSON_FILE)) {
    console.error(`❌ File not found: ${JSON_FILE}`);
    process.exit(1);
}

const data = JSON.parse(fs.readFileSync(JSON_FILE, 'utf8'));

// Schema compatible avec api.ts
const dropTable = `DROP TABLE IF EXISTS geometries;`;
const createTable = `
CREATE TABLE geometries (
    id TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    color TEXT,
    position_x REAL, position_y REAL, position_z REAL,
    rotation_x REAL, rotation_y REAL, rotation_z REAL,
    scale_x REAL, scale_y REAL, scale_z REAL,
    visible INTEGER,
    model_url TEXT
);`;

fs.writeFileSync('temp_import.sql', dropTable + createTable);

data.forEach(g => {
    const vals = [
        `'${g.id}'`,
        `'${g.name || 'Unnamed'}'`,
        `'${g.type || 'gltf_model'}'`,
        `'${g.color || '#ffffff'}'`,
        g.position?.x || 0, g.position?.y || 0, g.position?.z || 0,
        g.rotation?.x || 0, g.rotation?.y || 0, g.rotation?.z || 0,
        g.scale?.x || 1, g.scale?.y || 1, g.scale?.z || 1,
        g.visible ? 1 : 0,
        `'${g.model_url || ''}'`
    ];
    fs.appendFileSync('temp_import.sql', `INSERT INTO geometries VALUES (${vals.join(',')});\n`);
});

try {
    execSync(`sqlite3 ${DB_FILE} < temp_import.sql`);
    console.log(`✅ Successfully imported ${data.length} items into ${DB_FILE}`);
} catch (e) {
    console.error(`❌ Error during import:`, e.message);
} finally {
    if (fs.existsSync('temp_import.sql')) fs.unlinkSync('temp_import.sql');
}
