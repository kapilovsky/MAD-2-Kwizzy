<script setup>
import Sidebar from "@/components/Student/StudentSidebar.vue";
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import arrow from "../../assets/images/icons/Arrow.png";
import check from "../../assets/images/icons/check.svg";

const route = useRoute();
const student = ref(null);
const isLoading = ref(true);
const recentQuizzes = ref([]);
const student_id = parseInt(route.params.id);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(student_id);
    recentQuizzes.value = await studentService.getRecentActivity(student_id);
    console.log(student.value);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(() => {
  fetchStudent();
});
</script>

<template>
  <div class="min-h-screen">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <Loader />
    </div>

    <Sidebar v-else-if="student" :student="student">
      <div class="mb-10 flex gap-4">
        <div class="relative overflow-hidden">
          <div
            v-if="!student.student_info.profile_pic"
            class="w-36 h-36 rounded-lg bg-[#192227] text-white/20 hover:text-white/40 transition-all duration-200"
          >
            <span class="absolute -bottom-6 right-0 text-9xl">{{
              student.student_info.name.charAt(0)
            }}</span>
          </div>
        </div>
        <div>
          <h2 class="text-4xl sohne-mono tracking-tight py-2 font-bold">
            HELLO, {{ student.student_info.name }}✨
          </h2>
          <p class="text-neutral-600 sohne-mono text-sm">
            {{ getCurrentTimeGreeting() }} • {{ getCurrentDate() }}
          </p>
          <div class="font-mono text-xs text-gray-400 mt-2">
            {{ student.student_info.qualification.toUpperCase() }}
          </div>
          <div class="font-mono text-xs text-gray-400 mt-2">
            ID: #{{ student.student_info.id.toString().padStart(4, "0") }}
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Performance Card -->
        <div
          class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#192227] overflow-hidden relative group"
        >
          <div
            class="absolute -top-10 -right-32 opacity-10 group-hover:opacity-20 transition-all duration-200"
          >
            <img :src="arrow" class="w-[70%]" alt="" />
          </div>
          <h3
            class="font-mono font-medium uppercase text-sm tracking-wider text-[#e0f2ff] mb-4"
          >
            Performance
          </h3>
          <div
            class="text-5xl sohne font-bold bg-gradient-to-r from-[#e0f2ff] bg-clip-text text-transparent"
          >
            {{ student.student_info.quiz_stats.performance_percentage }}%
          </div>
          <p class="sohne-mono text-xs text-[#e0f2ff]/70 mt-2 uppercase">
            Keep up the good work
          </p>
        </div>

        <!-- Activity Card -->
        <div
          class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#fff9f0] overflow-hidden relative group"
        >
          <div
            class="absolute -top-40 -right-40 text-[340px] opacity-10 group-hover:opacity-30 transition-all duration-300"
          >
            ⚡️
          </div>
          <h3
            class="font-mono font-medium uppercase text-sm tracking-wider text-orange-600 mb-4"
          >
            Last Active
          </h3>
          <div class="text-5xl sohne font-bold text-orange-600">
            {{ formatDate(student.student_info.quiz_stats.last_active) }}
          </div>
          <p class="font-mono text-xs text-orange-500 mt-2 uppercase">
            Keep the momentum
          </p>
        </div>
        <div
          class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#192227] overflow-hidden relative group"
        >
          <div
            class="absolute -top-24 -right-16 text-6xl opacity-10 group-hover:opacity-30 transition-all duration-300"
          >
            <component :is="check" class="fill-[#fff] w-[400px] h-[400px]" />
          </div>
          <h3
            class="font-mono font-medium uppercase text-sm tracking-wider text-[#f0f7ff] mb-4"
          >
            Completed
          </h3>
          <div
            class="text-5xl sohne font-bold bg-gradient-to-r from-[#e0f2ff] bg-clip-text text-transparent"
          >
            {{ student.student_info.quiz_stats.total_quizzes_attempted }}
          </div>
          <p class="font-mono text-xs text-[#f0f7ff]/70 mt-2 uppercase">
            quizzes attempted
          </p>
        </div>
      </div>

      <!-- Recent Activity -->
      <div
        class="rounded-3xl px-8 py-3 shadow-sm transition-all hover:shadow-lg bg-[#fff9f0]"
      >
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-bold text-[48px] text-orange-600 tracking-tighter">
            Recent Activity
          </h3>
          <span class="text-sm text-orange-600 sohne-mono font-bold"
            >+ VIEW MORE</span
          >
        </div>
        <table class="w-full border-collapse">
          <thead>
            <tr
              class="text-left text-orange-600 text-sm border-b-2 border-black"
            >
              <th class="p-2">Quiz Title</th>
              <th class="p-2">Score</th>
              <th class="p-2">Accuracy</th>
              <th class="p-2">Completion Date</th>
              <th class="text-right p-2">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in recentQuizzes" :key="quiz.id">
              <td class="p-2">{{ quiz.quiz_name }}</td>
              <td class="p-2">{{ quiz.marks_scored }}</td>
              <td class="p-2">{{ quiz.percentage }}%</td>
              <td class="p-2">{{ formatDate(quiz.completed_at) }}</td>
              <td class="text-right">
                <button
                  class="text-orange-500 hover:font-bold text-sm sohne-mono bg-orange-200 px-5 py-1 rounded-md"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Sidebar>
  </div>
</template>

<style scoped>
.hover-scale {
  transition: transform 0.2s;
}

.hover-scale:hover {
  transform: scale(1.02);
}

.font-mono {
  font-family: "IBM Plex Mono";
}

tbody tr {
  transition: all 0.15s ease;
}

tbody tr:hover {
  background-color: #ffecd0;
}
</style>
