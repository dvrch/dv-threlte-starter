import fs from 'fs';
import path from 'path';

const API_URL = process.env.VITE_PUBLIC_API_URL || 'https://dv-threlte-starter-backend.up.railway.app';
const STATIC_DIR = path.join(process.cwd(), 'static/data');

async function sync() {
    console.log(`📡 Fetching data from ${API_URL}/api/geometries/ ...`);
    try {
        const response = await fetch(`${API_URL}/api/geometries/`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        const results = Array.isArray(data) ? data : (data.results || []);

        if (!fs.existsSync(STATIC_DIR)) fs.mkdirSync(STATIC_DIR, { recursive: true });

        // 1. JSON brut pour le moteur Threlte
        fs.writeFileSync(path.join(STATIC_DIR, 'geometries.json'), JSON.stringify(results, null, 2));

        // 2. Format "Database Dump" plus lisible
        const dbDump = {
            metadata: {
                exported_at: new Date().toISOString(),
                source: API_URL,
                items_count: results.length
            },
            tables: {
                geometries: results
            }
        };
        fs.writeFileSync(path.join(STATIC_DIR, 'database.json'), JSON.stringify(dbDump, null, 2));

        // 3. 🎨 Bonus : Un fichier HTML d'Inventaire pour "voir les objets"
        const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inventory DB</title>
            <style>
                body { font-family: sans-serif; background: #121212; color: #eee; padding: 20px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
                th { background: #1e1e1e; color: #4db6ac; }
                tr:hover { background: #252525; }
                .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; background: #4db6ac; color: black; }
            </style>
        </head>
        <body>
            <h1>📦 Inventaire Géométries (Echo DB)</h1>
            <p>Dernière synchro : ${dbDump.metadata.exported_at}</p>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nom</th>
                        <th>Type</th>
                        <th>Position</th>
                        <th>Couleur</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(g => `
                        <tr>
                            <td><code>${g.id}</code></td>
                            <td><strong>${g.name}</strong></td>
                            <td><span class="badge">${g.type}</span></td>
                            <td>${g.position?.x}, ${g.position?.y}, ${g.position?.z}</td>
                            <td><div style="width:20px;height:20px;background:${g.color};border-radius:50%"></div></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </body>
        </html>`;
        fs.writeFileSync(path.join(STATIC_DIR, 'inventory.html'), html);

        console.log(`✅ Database synced! 
   - geometries.json (Engine)
   - database.json (Structure Dump)
   - inventory.html (Visual list)`);
    } catch (error) {
        console.error('❌ Failed to sync database:', error.message);
        process.exit(0);
    }
}

sync();
