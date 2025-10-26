import { writable } from 'svelte/store';

export const createMotionStore = (initialState) => {
  const { subscribe, set, update } = writable(initialState);
  
  return {
    subscribe,
    fadeIn: (direction, type, delay, duration) => {
      return {
        hidden: {
          x: direction === "left" ? 100 : direction === "right" ? -100 : 0,
          y: direction === "up" ? 100 : direction === "down" ? -100 : 0,
          opacity: 0,
        },
        visible: {
          x: 0,
          y: 0,
          opacity: 1,
          transition: {
            type,
            delay,
            duration,
            ease: "easeOut",
          },
        },
      };
    }
  };
}; 