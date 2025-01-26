// stores/breadcrumbsStore.js
import { defineStore } from "pinia";

export const BreadcrumbsStore = defineStore("breadcrumb", {
  state: () => ({
    subjectName: null,
    chapterName: null,
    subjectId: null,
    chapterId: null,
  }),

  actions: {
    setBreadcrumbs(data) {
      this.subjectName = data.subjectName;
      this.chapterName = data.chapterName;
      this.subjectId = data.subjectId;
      this.chapterId = data.chapterId;
    },

    clearBreadcrumbs() {
      this.subjectName = null;
      this.chapterName = null;
      this.subjectId = null;
      this.chapterId = null;
    },
  },

  persist: {
    key: "breadcrumbs",
    storage: localStorage,
  },
});
