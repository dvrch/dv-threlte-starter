import fs from 'fs';
import path from 'path';

const API_URL = process.env.VITE_PUBLIC_API_URL || 'https://dv-threlte-starter-backend.up.railway.app';
const OUTPUT_FILE = path.join(process.cwd(), 'static/data/geometries.json');

async function sync() {
    console.log(`📡 Fetching data from ${API_URL}/api/geometries/ ...`);
    try {
        const response = await fetch(`${API_URL}/api/geometries/`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        const results = Array.isArray(data) ? data : (data.results || []);

        // Ensure static/data directory exists
        const dir = path.dirname(OUTPUT_FILE);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

        fs.writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));
        console.log(`✅ successfully exported ${results.length} geometries to ${OUTPUT_FILE}`);
    } catch (error) {
        console.error('❌ Failed to sync database:', error.message);
        console.log('⚠️ Using existing local file if available.');
        process.exit(0); // Don't fail the build if backend is down
    }
}

sync();
