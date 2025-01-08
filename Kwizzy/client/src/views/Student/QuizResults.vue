<template>
  <div class="min-h-screen bg-[#fafafa] p-8">
    <!-- Loading State -->
    <div
      v-if="quizResultStore.isLoading"
      class="flex justify-center items-center h-64"
    >
      <Loader />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-2xl mx-auto">
      <div class="bg-red-50 border border-red-200 rounded-3xl p-8 text-center">
        <h2 class="text-red-600 text-xl sohne-mono mb-2">{{ error }}</h2>
        <button
          @click="backToDashboard"
          class="mt-4 px-6 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors sohne-mono"
        >
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- Results Content -->
    <div v-else-if="quizResult" class="max-w-4xl mx-auto">
      <!-- Quiz Header -->
      <div class="bg-[#192227] rounded-3xl p-8 mb-8 text-white">
        <div
          class="flex flex-col md:flex-row justify-between items-center md:items-center mb-8"
        >
          <div>
            <h1
              class="text-4xl sohne-mono font-bold mb-2 text-center md:text-left"
            >
              {{ quizResult.quiz_name }}
            </h1>
            <p class="text-gray-400 text-center md:text-left">
              {{ quizResult.quiz_description }}
            </p>
          </div>
          <div class="mt-4 md:mt-0 text-right">
            <p class="text-sm text-gray-400 font-mono">Completed on</p>
            <p class="font-medium text-[#e0f2ff] text-xs md:text-base">
              {{ quizResult.completed_at_formatted }}
            </p>
          </div>
        </div>

        <!-- Score Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Score Card -->
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 text-center">
            <h3 class="text-gray-400 font-mono text-sm uppercase mb-2">
              Score
            </h3>
            <div class="text-4xl font-bold text-[#e0f2ff]">
              {{ quizResult.marks_scored }}/{{ quizResult.total_marks }}
            </div>
          </div>

          <!-- Percentage Card -->
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 text-center">
            <h3 class="text-gray-400 font-mono text-sm uppercase mb-2">
              Accuracy
            </h3>
            <div
              class="text-4xl font-bold"
              :class="{
                'text-green-400': percentage >= 70,
                'text-yellow-400': percentage >= 40 && percentage < 70,
                'text-red-400': percentage < 40,
              }"
            >
              {{ percentage }}%
            </div>
          </div>

          <!-- Status Card -->
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 text-center">
            <h3 class="text-gray-400 font-mono text-sm uppercase mb-2">
              Status
            </h3>
            <div
              class="text-2xl font-bold"
              :class="percentage >= 70 ? 'text-green-400' : 'text-red-400'"
            >
              {{ percentage >= 70 ? "PASSED" : "FAILED" }}
            </div>
          </div>
        </div>
      </div>

      <!-- Answer Review -->
      <div class="bg-white rounded-3xl shadow-sm p-8">
        <h2 class="text-3xl sohne-mono font-bold mb-8 text-center md:text-left">
          Answer Review
        </h2>

        <div class="space-y-6">
          <div
            v-for="answer in quizResult.user_answers"
            :key="answer.id"
            class="border rounded-2xl overflow-hidden transition-all duration-200 hover:shadow-md"
          >
            <div
              class="p-6"
              :class="answer.is_correct ? 'bg-[#192227]' : 'bg-red-50'"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                  <div
                    class="w-10 h-10 rounded-full flex items-center justify-center text-lg"
                    :class="
                      answer.is_correct
                        ? 'bg-green-500 text-white'
                        : 'bg-red-500 text-white'
                    "
                  >
                    <component
                      v-if="answer.is_correct"
                      :is="Check"
                      class="w-6 h-6 fill-white"
                    />
                    <component v-else :is="Cross" class="w-6 h-6 fill-[#fff]" />
                  </div>
                  <div>
                    <p
                      class="font-medium"
                      :class="
                        answer.is_correct ? 'text-white' : 'text-gray-900'
                      "
                    >
                      Question {{ answer.question_id }}
                    </p>
                    <p
                      class="text-sm"
                      :class="
                        answer.is_correct ? 'text-gray-400' : 'text-gray-500'
                      "
                    >
                      {{
                        answer.is_correct
                          ? "Correct Answer"
                          : "Incorrect Answer"
                      }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 bg-white">
              <div class="space-y-4">
                <div>
                  <p class="text-sm text-gray-500 font-mono uppercase mb-2">
                    Your Answer
                  </p>
                  <p class="font-medium">Option {{ answer.selected_option }}</p>
                </div>
                <div v-if="!answer.is_correct">
                  <p class="text-sm text-gray-500 font-mono uppercase mb-2">
                    Correct Answer
                  </p>
                  <p class="font-medium text-green-600">
                    Option {{ answer.correct_option }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col md:flex-row justify-between gap-4 mt-8">
        <button
          @click="backToDashboard"
          class="px-6 py-3 bg-[#192227] text-white rounded-xl hover:bg-[#2a3b44] transition-colors sohne-mono"
        >
          ← Back to Dashboard
        </button>

        <button
          @click="shareResults"
          class="px-6 py-3 bg-blue-100 text-blue-700 rounded-xl hover:bg-blue-200 transition-colors sohne-mono"
        >
          Share Results
        </button>
      </div>
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
import Check from "../../assets/images/icons/check.svg";
import Cross from "../../assets/images/icons/x-circle.svg";

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

const backToDashboard = async () => {
  try {
    await router.push(`/student/${route.params.id}`);
    window.location.reload(); // Force reload after navigation
  } catch (error) {
    console.error("Navigation error:", error);
    toast.error("Error returning to dashboard");
  }
};

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
