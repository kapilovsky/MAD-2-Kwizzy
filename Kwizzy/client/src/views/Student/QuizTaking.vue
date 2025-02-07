<!-- components/QuizTaking.vue -->
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

const handleSubmit = async () => {
  if (isSubmitting.value) return;

  try {
    isSubmitting.value = true;

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
      localStorage.removeItem("quizStartTime");
      localStorage.removeItem("totalDuration");
      localStorage.removeItem("quizEndTime");
      await quizResultStore.clearResult();
      await quizResultStore.fetchResult(response.data.result.result_id);

      // Show success message
      toast.success("Quiz submitted successfully!");

      await router.push({
        name: "quiz-results",
        params: {
          id: route.params.id,
          quizId: route.params.quizId,
        },
        query: {
          resultId: response.data.result.result_id,
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
    const quizData = await quizStore.fetchQuiz(quizId);

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
    toast.success("Quiz has started, good luck!");
  } catch (error) {
    console.error("Error fetching quiz:", error);
    toast.error("Error loading quiz");
    router.push(`/student/${studentId}`);
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
  <div class="min-h-screen bg-[#fbfbff] p-8 rounded-3xl">
    <!-- Loading State -->
    <div
      v-if="quizStore.isLoading"
      class="flex justify-center items-center h-64"
    >
      <div class="spinner">Loading...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="quizStore.error" class="max-w-2xl mx-auto text-center">
      <div class="bg-red-50 border border-red-200 rounded-3xl p-8">
        <p class="text-red-600 sohne-mono">{{ quizStore.error }}</p>
        <button
          @click="router.push(`/student/${studentId}`)"
          class="mt-6 px-6 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors sohne-mono"
        >
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- Quiz Interface -->
    <div
      v-else-if="quizStore.isQuizReady && currentQuestion"
      class="max-w-4xl mx-auto"
    >
      <!-- Quiz Header -->
      <div class="mb-8 flex justify-between items-center">
        <div>
          <h1 class="text-4xl tracking-tighter font-bold">{{ quiz.name }}</h1>
          <p class="text-gray-600 sohne-mono mt-2">{{ quiz.description }}</p>
        </div>
        <!-- Timer Card -->
        <div
          class="bg-[#192227] rounded-2xl sm:p-6 sm:min-w-[200px] p-5 text-center"
          :class="{ 'animate-pulse': timeRemaining < 300 }"
        >
          <h3
            class="font-mono uppercase text-sm tracking-wider text-[#e0f2ff] mb-2"
          >
            Time Remaining
          </h3>
          <div
            class="text-3xl sohne font-bold"
            :class="{
              'text-red-400': timeRemaining < 300,
              'text-[#e0f2ff]': timeRemaining >= 300,
            }"
          >
            {{ formatTime(timeRemaining) }}
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm sohne-mono text-gray-700">
            Question {{ questionProgress.current }} of
            {{ questionProgress.total }}
          </span>
          <span class="text-sm sohne-mono text-gray-700">
            {{
              Math.round(
                (questionProgress.current / questionProgress.total) * 100
              )
            }}% Complete
          </span>
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            class="h-full bg-[#192227] transition-all duration-300"
            :style="{
              width: `${
                (questionProgress.current / questionProgress.total) * 100
              }%`,
            }"
          ></div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="bg-white rounded-3xl shadow-sm px-8 py-6 mb-6">
        <h2 class="text-2xl font-bold mb-6">{{ currentQuestion.title }}</h2>
        <p class="text-gray-700 mb-8">Q. {{ currentQuestion.text }}</p>

        <!-- Options -->
        <div class="space-y-4">
          <div
            v-for="option in currentQuestion.options"
            :key="option.id"
            @click="selectOption(currentQuestion.id, option.id)"
            class="px-6 py-5 rounded-2xl border-2 cursor-pointer transition-all duration-200"
            :class="{
              'border-[#192227] bg-[#192227] text-white':
                userAnswers.get(currentQuestion.id) === option.id,
              'border-gray-200 hover:border-[#192227] hover:bg-gray-50':
                userAnswers.get(currentQuestion.id) !== option.id,
            }"
          >
            <div class="flex items-center gap-4">
              <div
                class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                :class="{
                  'border-white':
                    userAnswers.get(currentQuestion.id) === option.id,
                  'border-gray-400':
                    userAnswers.get(currentQuestion.id) !== option.id,
                }"
              >
                <div
                  v-if="userAnswers.get(currentQuestion.id) === option.id"
                  class="w-3 h-3 bg-white rounded-full"
                ></div>
              </div>
              <span class="flex-1">{{ option.text }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex justify-between items-center">
        <button
          @click="previousQuestion"
          :disabled="isFirstQuestion"
          class="px-6 py-3 rounded-xl sohne-mono text-sm transition-all duration-200"
          :class="
            isFirstQuestion
              ? 'text-gray-400 cursor-not-allowed'
              : 'text-gray-700 hover:bg-gray-100'
          "
        >
          🡰 Previous
        </button>

        <div class="flex gap-4">
          <button
            v-if="!isLastQuestion"
            @click="nextQuestion"
            class="px-6 py-3 bg-[#192227] text-white rounded-xl sohne-mono text-sm hover:bg-[#2a3b44] transition-colors"
          >
            Next 🡲
          </button>
          <button
            v-else
            @click="handleSubmit"
            :disabled="isSubmitting"
            class="px-6 py-3 bg-green-600 text-white rounded-xl sohne-mono text-sm hover:bg-green-700 transition-colors disabled:opacity-50"
          >
            {{ isSubmitting ? "Submitting..." : "Submit Quiz" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Add your existing font classes */
.sohne {
  font-family: sohne;
}

.sohne-mono {
  font-family: sohne-mono;
}

.font-mono {
  font-family: "IBM Plex Mono";
}
</style>
