// composables/useCursor.js
export const useCursor = () => {
  const addCursorState = (className) => {
    document.querySelector(".cursor-dot").classList.add(className);
    document.querySelector(".cursor-outline").classList.add(className);
  };

  const removeCursorState = (className) => {
    document.querySelector(".cursor-dot").classList.remove(className);
    document.querySelector(".cursor-outline").classList.remove(className);
  };

  return {
    addCursorState,
    removeCursorState,
  };
};
