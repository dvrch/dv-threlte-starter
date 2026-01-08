import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const API_URL = process.env.VITE_PUBLIC_API_URL || 'https://dv-threlte-starter-backend.up.railway.app';
const STATIC_DIR = path.join(process.cwd(), 'static/data');
const DB_FILE = path.join(STATIC_DIR, 'inventory.db');

async function sync() {
    console.log(`📡 Fetching data from ${API_URL}/api/...`);
    try {
        // 1. Fetch Geometries
        const geoResponse = await fetch(`${API_URL}/api/geometries/`);
        const geoData = await geoResponse.json();
        const geometries = Array.isArray(geoData) ? geoData : (geoData.results || []);

        // 2. Fetch Types
        const typeResponse = await fetch(`${API_URL}/api/types/`);
        const types = await typeResponse.json();
        const typeList = Array.isArray(types) ? types : (types.results || []);

        if (!fs.existsSync(STATIC_DIR)) fs.mkdirSync(STATIC_DIR, { recursive: true });

        // Sauvegarde des JSON
        fs.writeFileSync(path.join(STATIC_DIR, 'geometries.json'), JSON.stringify(geometries, null, 2));
        fs.writeFileSync(path.join(STATIC_DIR, 'types.json'), JSON.stringify(typeList, null, 2));

        // 🗄️ Création de la VRAIE Base de Données SQLite (.db)
        console.log(`🔨 Creating SQLite database at ${DB_FILE} ...`);
        if (fs.existsSync(DB_FILE)) fs.unlinkSync(DB_FILE);

        const sqlScriptPath = path.join(STATIC_DIR, 'import.sql');
        let sqlCommands = `
CREATE TABLE types (id TEXT PRIMARY KEY, name TEXT);
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
);
`;

        typeList.forEach(t => {
            sqlCommands += `INSERT INTO types VALUES ('${t.id}', '${t.id}');\n`;
        });

        geometries.forEach(g => {
            sqlCommands += `INSERT INTO geometries VALUES ('${g.id}', '${g.name?.replace(/'/g, "''")}', '${g.type}', '${g.color}', ${g.position?.x || 0}, ${g.position?.y || 0}, ${g.position?.z || 0}, ${g.rotation?.x || 0}, ${g.rotation?.y || 0}, ${g.rotation?.z || 0}, ${g.scale?.x || 1}, ${g.scale?.y || 1}, ${g.scale?.z || 1}, ${g.visible ? 1 : 0}, '${g.model_url || ''}');\n`;
        });

        fs.writeFileSync(sqlScriptPath, sqlCommands);

        try {
            execSync(`sqlite3 ${DB_FILE} < ${sqlScriptPath}`);
            console.log(`✅ SQLite DB created successfully!`);
            fs.unlinkSync(sqlScriptPath);
        } catch (sqliteError) {
            console.error('⚠️ sqlite3 fail:', sqliteError.message);
        }

        // 🎨 Inventaire HTML
        const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inventory DB</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; background: #1e293b; margin-top: 20px; border-radius: 8px; overflow: hidden; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #334155; }
                th { background: #334155; color: #38bdf8; }
                .badge { padding: 3px 8px; border-radius: 12px; font-size: 0.8em; background: #0ea5e9; }
                .color { width: 20px; height: 20px; border-radius: 4px; border: 1px solid #fff; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📦 Inventaire de la Base de Données</h1>
                <p>Date sync : ${new Date().toLocaleString()}</p>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Nom</th><th>Type</th><th>Position</th><th>Couleur</th></tr>
                    </thead>
                    <tbody>
                        ${geometries.map(g => `
                            <tr>
                                <td><code>${g.id}</code></td>
                                <td><strong>${g.name}</strong></td>
                                <td><span class="badge">${g.type}</span></td>
                                <td>${(g.position?.x || 0).toFixed(1)}, ${(g.position?.y || 0).toFixed(1)}, ${(g.position?.z || 0).toFixed(1)}</td>
                                <td><div class="color" style="background:${g.color}"></div></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </body>
        </html>`;
        fs.writeFileSync(path.join(STATIC_DIR, 'inventory.html'), html);

        console.log(`✅ Everything synced! (JSONs, .db, .html)`);
    } catch (error) {
        console.error('❌ Sync failed:', error.message);
        process.exit(0);
    }
}

sync();
