// Create a new eventBus.js file
import { ref } from "vue";
import { defineStore } from "pinia";

export const useEventStore = defineStore("events", () => {
  const shouldRefreshSubjects = ref(false);

  function triggerSubjectRefresh() {
    shouldRefreshSubjects.value = true;
  }

  function resetSubjectRefresh() {
    shouldRefreshSubjects.value = false;
  }

  return {
    shouldRefreshSubjects,
    triggerSubjectRefresh,
    resetSubjectRefresh,
  };
});
