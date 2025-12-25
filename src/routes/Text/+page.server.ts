import fs from 'fs';
import path from 'path';

export const load = async () => {
    const filePath = path.resolve('static/Text/cv-en.md');
    const content = fs.readFileSync(filePath, 'utf-8');

    // Simple parsing to split into lines or sections
    const lines = content.split('\n').filter(line => line.trim() !== '');

    return {
        cvLines: lines
    };
};
