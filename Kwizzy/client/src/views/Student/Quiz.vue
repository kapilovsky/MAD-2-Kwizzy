<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <Loader />
    </div>

    <div v-else-if="quiz">
      <div class="bg-[#192227] text-[#fdfcfc] p-6 rounded-2xl shadow">
        <div class="flex justify-between">
          <div class="space-y-4">
            <div>
              <h1 class="text-3xl font-bold">{{ quiz?.name }}</h1>
              <p class="text-gray-300 mt-2">{{ quiz?.description }}</p>
            </div>
            <div class="flex gap-8">
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Duration</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.time_duration }}
                </p>
              </div>
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Price</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.price ? `₹${quiz.price}` : "Free" }}
                </p>
              </div>
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Questions</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.questions?.length || 0 }}
                </p>
              </div>
            </div>
          </div>
          <div
            class="text-[560px] absolute bottom-0 right-0 opacity-20 z-1 select-none"
            style="pointer-events: none"
          >
            🡽
          </div>
        </div>

        <div>
          <h3 class="sohne-mono text-lg mb-2">Instructions</h3>
          <ul class="sohne">
            <li>🡪 You cannot pause the quiz once started</li>
            <li>🡪 Timer will continue even if you close the browser</li>
            <li>🡪 Each question has only one correct answer</li>
            <li>🡪 You can review your answers before final submission</li>
          </ul>
        </div>

        <button
          @click="showStartDialog"
          class="w-full bg-[#fdfcfc] py-3 rounded-lg transition-colors disabled:bg-gray-400 mt-8 text-right relative group overflow-hidden"
          :disabled="isStarting"
        >
          <span class="arame text-5xl mr-20 cursor-pointer text-[#192227]"
            >Start Quiz</span
          ><span
            class="absolute text-5xl right-7 top-1/2 transform -translate-y-1/2 text-[#192227] opacity-0 group-hover:opacity-100 group-hover:translate-x-2 transition-all"
          >
            🡲
          </span>
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <!-- Start Quiz Dialog -->
    <transition name="fade" mode="out-in">
      <DialogModal
        v-if="isDialogOpen"
        @close="isDialogOpen = false"
        @confirm="startQuiz"
      >
        <template #title>Start Quiz</template>
        <template #content>
          <p class="font-mono font-semibold tracking-tighter text-lg">
            Are you ready to start the quiz? Once started:
          </p>
          <ul class="list-disc list-inside font-medium tracking-[-0.5px]">
            <li>The timer will begin immediately.</li>
            <li>You cannot pause or restart.</li>
            <li>Make sure you have a stable internet connection.</li>
          </ul>
        </template>
        <template #actions>
          <button
            class="px-4 py-2 text-orange-600 font-bold"
            @click="isDialogOpen = false"
          >
            Cancel
          </button>
          <button
            @click="startQuiz"
            class="px-4 py-2 bg-orange-200 text-orange-600 rounded-xl hover:bg-[#ffe4bb] hover:text-orange-700 transition-all duration-300 font-bold"
          >
            Start Now
          </button>
        </template>
      </DialogModal>
    </transition>
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

    router.push(`${route.path}/take`);
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

<style scoped>
.arame {
  font-family: arame;
}
</style>
