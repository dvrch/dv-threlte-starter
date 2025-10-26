
import { writable } from 'svelte/store';


export const FilmStore = writable([]);


// en ypescript
// import { writable } from 'svelte/store';

// interface Film {
//     id: number;
//     title: string;
//     director: string;
//     releaseYear: number;
// }

// export const FilmStore = writable<Film[]>([]);