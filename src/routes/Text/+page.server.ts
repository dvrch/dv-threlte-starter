// @ts-ignore
import cvContent from './cv-en.md?raw';

export const load = async () => {
    // Vite raw import ensures the text is bundled, no fs needed! 📦
    const lines = cvContent.split('\n').filter((line: string) => line.trim() !== '');

    return {
        cvLines: lines
    };
};
