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

    isQuizInProgress: () => {
      const startTime = localStorage.getItem("quizStartTime");
      const endTime = localStorage.getItem("quizEndTime");
      if (!startTime || !endTime) return false;

      const now = new Date().getTime();
      return now < parseInt(endTime);
    },
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
    async checkQuizStatus(quizId) {
      const startTime = localStorage.getItem("quizStartTime");
      const endTime = localStorage.getItem("quizEndTime");

      if (startTime && endTime) {
        const now = new Date().getTime();
        if (now >= parseInt(endTime)) {
          // Quiz time has expired
          await this.handleExpiredQuiz(quizId);
          return false;
        }
        return true;
      }
      return false;
    },
    async handleExpiredQuiz(quizId) {
      // Automatically submit quiz if time expired
      const answers = Array.from(this.userAnswers.entries()).map(
        ([questionId, optionId]) => ({
          question_id: parseInt(questionId),
          selected_option_id: parseInt(optionId),
        })
      );

      try {
        const response = await axios.post(
          `${API_URL}/user-answers`,
          {
            quiz_id: quizId,
            answers: answers,
            expired: true,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Clear timer data
        localStorage.removeItem("quizStartTime");
        localStorage.removeItem("totalDuration");
        localStorage.removeItem("quizEndTime");

        return response.data;
      } catch (error) {
        console.error("Error handling expired quiz:", error);
        throw error;
      }
    },
  },
});
