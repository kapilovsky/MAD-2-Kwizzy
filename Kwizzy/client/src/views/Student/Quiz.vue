<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <Loader />
    </div>

    <div v-else-if="quiz" class="max-w-2xl mx-auto">
      <!-- Quiz Details Card -->
      <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h1 class="text-3xl font-bold mb-4">{{ quiz.name }}</h1>
        <p class="text-gray-600 mb-4">{{ quiz.description }}</p>

        <div class="grid grid-cols-2 gap-4 mb-6">
          <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm text-gray-500">Duration</p>
            <p class="text-lg font-semibold">{{ quiz.time_duration }}</p>
          </div>
          <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm text-gray-500">Questions</p>
            <p class="text-lg font-semibold">
              {{ quiz.questions?.length || 0 }}
            </p>
          </div>
        </div>

        <!-- Instructions -->
        <div class="bg-blue-50 p-4 rounded-lg mb-6">
          <h3 class="font-semibold mb-2">Instructions:</h3>
          <ul class="list-disc list-inside text-sm text-gray-700">
            <li>You cannot pause the quiz once started</li>
            <li>Timer will continue even if you close the browser</li>
            <li>Each question has only one correct answer</li>
            <li>You can review your answers before final submission</li>
          </ul>
        </div>

        <!-- Start Quiz Button -->
        <button
          @click="showStartDialog"
          class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
          :disabled="isStarting"
        >
          {{ isStarting ? "Starting Quiz..." : "Start Quiz" }}
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <!-- Start Quiz Dialog -->
    <DialogModal
      v-if="isDialogOpen"
      @close="isDialogOpen = false"
      @confirm="startQuiz"
    >
      <template #title>Start Quiz</template>
      <template #content>
        <p>Are you ready to start the quiz? Once started:</p>
        <ul class="list-disc list-inside mt-2">
          <li>The timer will begin immediately</li>
          <li>You cannot pause or restart</li>
          <li>Make sure you have a stable internet connection</li>
        </ul>
      </template>
      <template #actions>
        <button
          @click="isDialogOpen = false"
          class="px-4 py-2 text-gray-600 hover:text-gray-800"
        >
          Cancel
        </button>
        <button
          @click="startQuiz"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Start Now
        </button>
      </template>
    </DialogModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useToast } from "@/composables/useToast";
import DialogModal from "@/components/DialogModal.vue";
import Loader from "@/components/Loader.vue";
const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const route = useRoute();
const toast = useToast();

const quiz = ref(null);
const error = ref(null);
const isLoading = ref(true);
const isStarting = ref(false);
const isDialogOpen = ref(false);
const student_id = route.params.id;

const fetchQuizDetails = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(
      `${API_URL}/quizzes/${route.params.quizId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    quiz.value = response.data;
  } catch (err) {
    console.error("Error fetching quiz:", err);
    error.value = "Failed to load quiz details";
    toast.error("Error loading quiz details");
  } finally {
    isLoading.value = false;
  }
};

const showStartDialog = () => {
  isDialogOpen.value = true;
};

const startQuiz = async () => {
  try {
    isStarting.value = true;
    isDialogOpen.value = false;

    // Navigate to quiz taking page
    router.push(`/student/${student_id}/quiz/${route.params.quizId}/take`);
  } catch (err) {
    console.error("Error starting quiz:", err);
    toast.error("Failed to start quiz");
    isStarting.value = false;
  }
};

onMounted(() => {
  fetchQuizDetails();
});
</script>
