// stores/quizStore.js
import { defineStore } from "pinia";

export const useQuizStore = defineStore("quiz", {
  state: () => ({
    quiz: null,
    currentQuestionIndex: 0,
    userAnswers: new Map(), // Store user's selected answers
    timeRemaining: null,
    quizStartTime: null,
  }),

  actions: {
    setQuiz(quizData) {
      this.quiz = quizData;
      // Initialize time if not already set
      if (!localStorage.getItem("quizStartTime")) {
        const [hours, minutes] = quizData.time_duration.split(":");
        const totalMinutes = parseInt(hours) * 60 + parseInt(minutes);
        localStorage.setItem("quizStartTime", new Date().getTime());
        localStorage.setItem("totalDuration", totalMinutes);
      }
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

    submitQuiz() {
      // Convert Map to array for API submission
      const answers = Array.from(this.userAnswers.entries()).map(
        ([questionId, optionId]) => ({
          question_id: questionId,
          selected_option_id: optionId,
        })
      );
      return answers;
    },
  },

  getters: {
    currentQuestion: (state) =>
      state.quiz?.questions[state.currentQuestionIndex] || null,

    isLastQuestion: (state) =>
      state.currentQuestionIndex === state.quiz?.questions.length - 1,

    isFirstQuestion: (state) => state.currentQuestionIndex === 0,

    questionProgress: (state) => ({
      current: state.currentQuestionIndex + 1,
      total: state.quiz?.questions.length || 0,
    }),
  },
});
