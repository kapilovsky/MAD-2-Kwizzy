// composables/useToast.js
import { useToastStore } from "@/stores/toastStore";

export function useToast() {
  const store = useToastStore();

  return {
    success(message, title = "") {
      store.addToast({
        title,
        message,
        type: "success",
        duration: 5000,
      });
    },

    error(message, title = "") {
      store.addToast({
        title,
        message,
        type: "error",
        duration: 7000,
      });
    },

    info(message, title = "") {
      store.addToast({
        title,
        message,
        type: "info",
        duration: 5000,
      });
    },

    warning(message, title = "") {
      store.addToast({
        title,
        message,
        type: "warning",
        duration: 6000,
      });
    },
  };
}
