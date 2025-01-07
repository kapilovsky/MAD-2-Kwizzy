import { defineStore } from "pinia";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const useQuizResultStore = defineStore("quizResult", {
  state: () => ({
    currentResult: null,
    isLoading: false,
    error: null,
  }),

  actions: {
    setResult(result) {
      console.log("Setting result in store:", result);
      this.currentResult = result;
    },

    async fetchResult(resultId) {
      this.isLoading = true;
      try {
        const token = localStorage.getItem("access_token");
        if (!token) throw new Error("No access token available");

        const response = await axios.get(
          `${API_URL}/quiz-results/${resultId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.currentResult = response.data;
        return response.data;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    clearResult() {
      this.currentResult = null;
      this.error = null;
    },
  },
});
