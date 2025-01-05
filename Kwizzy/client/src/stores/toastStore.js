// stores/toastStore.js
import { defineStore } from "pinia";

export const useToastStore = defineStore("toast", {
  state: () => ({
    toasts: [],
  }),

  actions: {
    addToast(toast) {
      const id = Date.now();
      this.toasts.push({
        id,
        title: toast.title,
        message: toast.message,
        type: toast.type || "info", // 'success', 'error', 'info', 'warning'
        duration: toast.duration || 5000,
      });

      // Remove toast after duration
      setTimeout(() => {
        this.removeToast(id);
      }, toast.duration || 5000);
    },

    removeToast(id) {
      this.toasts = this.toasts.filter((toast) => toast.id !== id);
    },
  },
});
