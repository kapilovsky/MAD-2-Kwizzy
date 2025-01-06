<script setup>
import Sidebar from "@/components/Student/StudentSidebar.vue";
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;

const route = useRoute();
const student = ref(null);
const quizzes = ref([]);
const isLoading = ref(true);
const student_id = parseInt(route.params.id);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(student_id);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchQuizzes = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");
    const response = await axios.get(`${API_URL}/quizzes`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    quizzes.value = response.data.quizzes;
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStudent();
  fetchQuizzes();
});

// Computed properties for stats
const completionRate = computed(() => {
  if (!student.value) return 0;
  const stats = student.value.student_info.quiz_stats;
  return stats.total_quizzes_attempted > 0
    ? (stats.quizzes_completed / stats.total_quizzes_attempted) * 100
    : 0;
});

const getCurrentTimeGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 18) return "Good Afternoon";
  return "Good Evening";
};

const getCurrentDate = () => {
  return new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<template>
  <div class="min-h-screen">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <Loader />
    </div>

    <Sidebar v-else-if="student" :student="student">
      <div class="mb-10">
        <h2 class="text-4xl sohne-mono tracking-tight py-2 font-bold">
          HELLO, {{ student.student_info.name }} ⚡️
        </h2>
        <p class="text-neutral-600 sohne-mono text-sm">
          {{ getCurrentTimeGreeting() }} • {{ getCurrentDate() }}
        </p>
      </div>

      <div>
        <h2 class="text-3xl sohne-mono tracking-tight py-2 font-bold">
          All Quizzes
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div
            v-for="quiz in quizzes"
            :key="quiz.id"
            class="bg-[#192227] text-[#fdfcfc] p-6 rounded-2xl shadow"
          >
            <RouterLink :to="`/student/${student_id}/quiz/${quiz.id}`">
              <h2 class="text-2xl font-bold mb-6 sohne-mono">
                {{ quiz.name }}
              </h2>
              <p class="text-sm font-medium sohne-mono">
                {{ quiz.description }}
              </p>
            </RouterLink>
          </div>
        </div>
      </div>
    </Sidebar>
  </div>
</template>

<style scoped>
.font-mono {
  font-family: "SF Mono", SFMono-Regular, ui-monospace, "DejaVu Sans Mono",
    Menlo, Consolas, monospace;
}
</style>
