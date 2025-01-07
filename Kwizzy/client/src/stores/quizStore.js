import { defineStore } from "pinia";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;

export const useQuizStore = defineStore("quiz", {
  state: () => ({
    quiz: null,
    currentQuestionIndex: 0,
    userAnswers: new Map(),
    isLoading: true,
    error: null,
  }),

  getters: {
    currentQuestion: (state) => {
      if (!state.quiz || !state.quiz.questions) return null;
      return state.quiz.questions[state.currentQuestionIndex] || null;
    },

    isLastQuestion: (state) => {
      if (!state.quiz || !state.quiz.questions) return false;
      return state.currentQuestionIndex === state.quiz.questions.length - 1;
    },

    isFirstQuestion: (state) => state.currentQuestionIndex === 0,

    questionProgress: (state) => ({
      current: state.currentQuestionIndex + 1,
      total: state.quiz?.questions?.length || 0,
    }),

    isQuizReady: (state) =>
      !state.isLoading && state.quiz !== null && !state.error,
  },

  actions: {
    async fetchQuiz(quizId) {
      this.isLoading = true;
      this.error = null;
      try {
        const token = localStorage.getItem("access_token");
        if (!token) throw new Error("No access token available");

        const response = await axios.get(`${API_URL}/quizzes/${quizId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.quiz = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to load quiz";
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    setQuiz(quizData) {
      this.quiz = quizData;
      this.currentQuestionIndex = 0;
      this.userAnswers.clear();
    },

    setAnswer(questionId, optionId) {
      this.userAnswers.set(questionId, optionId);
    },

    nextQuestion() {
      if (this.currentQuestionIndex < this.quiz.questions.length - 1) {
        this.currentQuestionIndex++;
      }
    },

    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },

    resetQuiz() {
      this.quiz = null;
      this.currentQuestionIndex = 0;
      this.userAnswers.clear();
      this.isLoading = false;
      this.error = null;
    },
  },
});
