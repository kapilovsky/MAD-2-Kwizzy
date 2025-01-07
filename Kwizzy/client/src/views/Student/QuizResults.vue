<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <!-- Loading State -->
    <div
      v-if="quizResultStore.isLoading"
      class="flex justify-center items-center h-64"
    >
      <Loader />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-2xl mx-auto px-4">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <h2 class="text-red-600 text-xl font-semibold mb-2">{{ error }}</h2>
        <button
          @click="router.push(`/student/${route.params.id}/dashboard`)"
          class="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- Results Content -->
    <div v-else-if="quizResult" class="max-w-4xl mx-auto px-4">
      <!-- Quiz Header -->
      <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div
          class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6"
        >
          <div>
            <h1 class="text-3xl font-bold mb-2">{{ quizResult.quiz_name }}</h1>
            <p class="text-gray-600">{{ quizResult.quiz_description }}</p>
          </div>
          <div class="mt-4 md:mt-0 text-right">
            <p class="text-sm text-gray-500">Completed on</p>
            <p class="font-medium">{{ quizResult.completed_at_formatted }}</p>
          </div>
        </div>

        <!-- Score Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Score -->
          <div class="bg-gray-50 rounded-lg p-6 text-center">
            <h3 class="text-gray-500 text-sm uppercase mb-2">Score</h3>
            <div class="text-4xl font-bold">
              {{ quizResult.marks_scored }}/{{ quizResult.total_marks }}
            </div>
          </div>

          <!-- Percentage -->
          <div class="bg-gray-50 rounded-lg p-6 text-center">
            <h3 class="text-gray-500 text-sm uppercase mb-2">Percentage</h3>
            <div
              class="text-4xl font-bold"
              :class="{
                'text-green-600': percentage >= 70,
                'text-yellow-600': percentage >= 40 && percentage < 70,
                'text-red-600': percentage < 40,
              }"
            >
              {{ percentage }}%
            </div>
          </div>

          <!-- Status -->
          <div class="bg-gray-50 rounded-lg p-6 text-center">
            <h3 class="text-gray-500 text-sm uppercase mb-2">Status</h3>
            <div
              class="text-2xl font-bold"
              :class="percentage >= 70 ? 'text-green-600' : 'text-red-600'"
            >
              {{ percentage >= 70 ? "PASSED" : "FAILED" }}
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Answers -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-semibold mb-6">Answer Review</h2>

        <div class="space-y-6">
          <div
            v-for="answer in quizResult.user_answers"
            :key="answer.id"
            class="border rounded-lg overflow-hidden"
          >
            <div
              class="p-4"
              :class="
                answer.is_correct
                  ? 'bg-green-50 border-green-200'
                  : 'bg-red-50 border-red-200'
              "
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span
                    class="w-8 h-8 rounded-full flex items-center justify-center text-white"
                    :class="answer.is_correct ? 'bg-green-500' : 'bg-red-500'"
                  >
                    {{ answer.is_correct ? "✓" : "✗" }}
                  </span>
                  <span class="font-medium"
                    >Question {{ answer.question_id }}</span
                  >
                </div>
                <span
                  class="px-3 py-1 rounded-full text-sm"
                  :class="
                    answer.is_correct
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                >
                  {{ answer.is_correct ? "Correct" : "Incorrect" }}
                </span>
              </div>
            </div>

            <div class="p-4 bg-white">
              <div class="mb-4">
                <p class="text-sm text-gray-500 mb-1">Selected Option:</p>
                <p class="font-medium">Option {{ answer.selected_option }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col md:flex-row justify-between gap-4 mt-6">
        <button
          @click="router.push(`/student/${route.params.id}`)"
          class="px-6 py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors text-gray-700 font-medium"
        >
          Back to Dashboard
        </button>
        <div class="flex gap-4">
          <button
            @click="shareResults"
            class="px-6 py-3 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors font-medium"
          >
            Share Results
          </button>
          <!-- <button
            @click="retakeQuiz"
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Retake Quiz
          </button> -->
        </div>
      </div>
    </div>
    <div v-else class="max-w-2xl mx-auto px-4 text-center">
      <p class="text-gray-600">No quiz result data available.</p>
      <button
        @click="fetchQuizResult"
        class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Retry Loading
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, watch, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import axios from "axios";
import { useToast } from "@/composables/useToast";
import Loader from "@/components/Loader.vue";
import { useQuizResultStore } from "@/stores/quizResultStore";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const route = useRoute();
const toast = useToast();
const quizResultStore = useQuizResultStore();

// Use storeToRefs for reactive store properties
const { currentResult, isLoading } = storeToRefs(quizResultStore);

const quizResult = ref(null);
const error = ref(null);

const quizId = route.params.quizId;
const studentId = route.params.id;
const quiz_result_id = route.query.resultId;

const percentage = computed(() => {
  if (!quizResult.value) return 0;
  return Math.round(
    (quizResult.value.marks_scored / quizResult.value.total_marks) * 100
  );
});

const fetchQuizResult = async () => {
  try {
    error.value = null;
    quizResultStore.isLoading = true;
    // If we have result in store, use it
    if (quizResultStore.currentResult) {
      console.log("Using result from store:", quizResultStore.currentResult);
      quizResult.value = quizResultStore.currentResult;
      return;
    }

    // If no result in store, fetch from API
    const resultId = route.query.resultId;
    if (!resultId) {
      throw new Error("No result ID provided");
    }

    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/quiz-results/${resultId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    quizResult.value = response.data;
    console.log("Fetched result from API:", response.data);
    quizResultStore.isLoading = false;
  } catch (err) {
    console.error("Error fetching quiz result:", err);
    error.value = err.message || "Failed to load quiz results";
    toast.error("Error loading quiz results");
  } finally {
    quizResultStore.isLoading = false;
  }
};

const shareResults = () => {
  if (!quizResult.value) return;

  const text = `I scored ${quizResult.value.marks_scored}/${quizResult.value.total_marks} (${percentage.value}%) in ${quizResult.value.quiz_name}!`;

  if (navigator.share) {
    navigator
      .share({
        title: "Quiz Results",
        text: text,
        url: window.location.href,
      })
      .catch(console.error);
  } else {
    navigator.clipboard
      .writeText(text)
      .then(() => toast.success("Results copied to clipboard!"))
      .catch(() => toast.error("Failed to copy results"));
  }
};

watch(
  [() => route.query.resultId, currentResult],
  ([newResultId, newResult]) => {
    if (newResult) {
      quizResult.value = newResult;
    } else if (newResultId) {
      fetchQuizResult();
    }
  },
  { immediate: true }
);

// Use both onMounted and watch for route changes
onMounted(() => {
  // Remove any existing beforeunload handlers
  window.onbeforeunload = null;
  fetchQuizResult();
});

onUnmounted(() => {
  // Clean up
  quizResultStore.clearResult();
});

// Watch for route changes
watch(
  () => route.query.resultId,
  (newResultId) => {
    if (newResultId) {
      fetchQuizResult();
    }
  }
);
</script>
