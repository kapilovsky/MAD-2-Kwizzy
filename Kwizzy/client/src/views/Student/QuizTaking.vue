<!-- components/QuizInterface.vue -->
<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import { useQuizResultStore } from "@/stores/quizResultStore";
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useToast } from "@/composables/useToast";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const route = useRoute();
const toast = useToast();
const quizStore = useQuizStore();
const quizResultStore = useQuizResultStore();

const timeRemaining = ref(null);
const isSubmitting = ref(false);
let timerInterval;
const quizId = route.params.quizId;
const studentId = route.params.id;

const {
  quiz,
  currentQuestion,
  isLastQuestion,
  isFirstQuestion,
  questionProgress,
  userAnswers,
} = storeToRefs(quizStore);

const { setQuiz, setAnswer, nextQuestion, previousQuestion, submitQuiz } =
  quizStore;

// Initialize timer
const initializeTimer = () => {
  const startTime = parseInt(localStorage.getItem("quizStartTime"));
  const totalDuration = parseInt(localStorage.getItem("totalDuration"));
  const endTime = parseInt(localStorage.getItem("quizEndTime"));

  if (!startTime || !endTime) return;

  const updateTimer = () => {
    const now = new Date().getTime();
    const remaining = Math.max(0, endTime - now) / 1000; // Convert to seconds

    if (remaining <= 0) {
      clearInterval(timerInterval);
      handleSubmit();
    } else {
      timeRemaining.value = Math.floor(remaining);
    }
  };

  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
};

const formatTime = (seconds) => {
  if (!seconds) return "00:00";
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
    .toString()
    .padStart(2, "0")}`;
};

const selectOption = (questionId, optionId) => {
  setAnswer(questionId, optionId);
};

const getQuestionButtonClass = (index) => {
  if (!quiz.value) return "";

  if (index === quizStore.currentQuestionIndex) {
    return "btn-primary";
  }
  return userAnswers.value.has(quiz.value.questions[index].id)
    ? "btn-success"
    : "btn-outline-secondary";
};

const handleSubmit = async () => {
  if (isSubmitting.value) return;

  try {
    isSubmitting.value = true;
    const loadingToast = toast.info("Submitting quiz...");

    // Format answers for API
    const answers = Array.from(userAnswers.value.entries()).map(
      ([questionId, optionId]) => ({
        question_id: parseInt(questionId),
        selected_option_id: parseInt(optionId),
      })
    );

    const payload = {
      quiz_id: quiz.value.id,
      answers: answers,
    };

    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    // Submit quiz to API
    const response = await axios.post(`${API_URL}/user-answers`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.data && response.status === 201) {
      // Store the result in both localStorage and Pinia store
      const quizResult = response.data.result;
      localStorage.setItem("quizResult", JSON.stringify(quizResult));
      quizResultStore.setResult(quizResult);

      // Clear quiz data
      localStorage.removeItem("quizStartTime");
      localStorage.removeItem("totalDuration");

      // Show success message
      toast.success("Quiz submitted successfully!");

      // Navigate to results page
      await router.replace({
        name: "quiz-results",
        params: {
          id: route.params.id,
          quizId: route.params.quizId,
        },
        query: {
          resultId: quizResult.result_id,
        },
      });
    }
  } catch (error) {
    console.error("Error submitting quiz:", error);
    toast.error(error.response?.data?.message || "Error submitting quiz");
  } finally {
    isSubmitting.value = false;
  }
};

const fetchQuizData = async () => {
  try {
    const quizData = await quizStore.fetchQuiz(route.params.quizId);

    const existingStartTime = localStorage.getItem("quizStartTime");
    const existingEndTime = localStorage.getItem("quizEndTime");

    if (!existingStartTime || !existingEndTime) {
      // Only set new timer if one doesn't exist
      const [hours, minutes] = quizData.time_duration.split(":");
      const totalMinutes = parseInt(hours) * 60 + parseInt(minutes);
      const startTime = new Date().getTime();
      const endTime = startTime + totalMinutes * 60 * 1000;

      localStorage.setItem("quizStartTime", startTime.toString());
      localStorage.setItem("totalDuration", totalMinutes.toString());
      localStorage.setItem("quizEndTime", endTime.toString());
    }

    initializeTimer();
    toast.success("Quiz loaded successfully");
  } catch (error) {
    console.error("Error fetching quiz:", error);
    toast.error("Error loading quiz");
    router.push("/dashboard");
  }
};

onMounted(() => {
  fetchQuizData();

  window.addEventListener("beforeunload", (e) => {
    if (timeRemaining.value > 0) {
      e.preventDefault();
    }
  });
});

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
  // Clear any quiz-related localStorage items
  localStorage.removeItem("quizStartTime");
  localStorage.removeItem("totalDuration");
  localStorage.removeItem("quizEndTime");
  window.removeEventListener("beforeunload", () => {});
  // Reset the store
  quizStore.resetQuiz();
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Loading State -->
    <div
      v-if="quizStore.isLoading"
      class="flex justify-center items-center h-screen"
    >
      <div class="spinner">Loading...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="quizStore.error" class="text-center">
      <p class="text-red-600">{{ quizStore.error }}</p>
      <button
        @click="router.push('/dashboard')"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Back to Dashboard
      </button>
    </div>

    <!-- Quiz Interface -->
    <div
      v-else-if="quizStore.isQuizReady && currentQuestion"
      class="max-w-3xl mx-auto"
    >
      <!-- Timer and Progress -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div class="progress" style="width: 70%">
              <div
                class="progress-bar"
                :style="{
                  width: `${
                    (questionProgress.current / questionProgress.total) * 100
                  }%`,
                }"
              >
                Question {{ questionProgress.current }} of
                {{ questionProgress.total }}
              </div>
            </div>
            <div class="timer" :class="{ 'text-danger': timeRemaining < 300 }">
              Time Remaining: {{ formatTime(timeRemaining) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="card">
        <div class="card-body">
          <h4 class="card-title mb-4">{{ currentQuestion.title }}</h4>
          <p class="card-text">{{ currentQuestion.text }}</p>

          <!-- Options -->
          <div class="options-container">
            <div
              v-for="option in currentQuestion.options"
              :key="option.id"
              class="option mb-3"
            >
              <div
                class="option-card p-3"
                :class="{
                  selected: userAnswers.get(currentQuestion.id) === option.id,
                }"
                @click="selectOption(currentQuestion.id, option.id)"
              >
                {{ option.text }}
              </div>
            </div>
          </div>

          <!-- Navigation -->
          <div class="d-flex justify-content-between mt-4">
            <button
              class="btn btn-secondary"
              @click="previousQuestion"
              :disabled="isFirstQuestion"
            >
              Previous
            </button>

            <button
              v-if="!isLastQuestion"
              class="btn btn-primary"
              @click="nextQuestion"
            >
              Next
            </button>
            <button
              v-else
              class="btn btn-success"
              @click="handleSubmit"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? "Submitting..." : "Submit Quiz" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Fallback State -->
    <div v-else class="text-center">
      <p>Unable to load quiz. Please try again.</p>
      <button
        @click="router.push('/dashboard')"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Back to Dashboard
      </button>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.timer {
  font-size: 1.2rem;
  font-weight: bold;
}

.option-card {
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-card:hover {
  background-color: #f8f9fa;
  border-color: #0d6efd;
}

.option-card.selected {
  background-color: #0d6efd;
  color: white;
  border-color: #0d6efd;
}

.question-navigator {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
