<!-- views/StudentDashboard.vue -->
<template>
  <div class="p-6">
    <Loader v-if="isLoading" />
    <div v-else>
      <h2
        @mouseover="addCursorState('heading-hover')"
        @mouseout="removeCursorState('heading-hover')"
        class="sm:text-5xl text-3xl mb-6 sohne-mono font-bold w-fit"
      >
        My Progress 📈
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Quizzes Taken
          </h3>
          <p class="text-3xl font-bold">{{ totalQuizzes }}</p>
        </div>
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Average Score
          </h3>
          <p class="text-3xl font-bold">{{ averageScore }}%</p>
        </div>
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Active Streak
          </h3>
          <p class="text-3xl font-bold">{{ currentStreak }} days</p>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SubjectPerformance :data="chartData.subject_performance" />
        <RecentPerformance :data="chartData.recent_performance" />
        <MonthlyProgress :data="chartData.monthly_progress" />
        <StrengthWeakness :data="chartData.strength_weakness" />
      </div>

      <!-- Activity Heatmap -->
      <div class="mt-6 bg-white rounded-xl p-6">
        <h3 class="text-xl mb-4 font-semibold">Activity Calendar</h3>
        <ActivityHeatmap :data="chartData.heatmap" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import { useCursor } from "@/composables/useCursor";
import SubjectPerformance from "@/components/Student/charts/SubjectPerformance.vue";
import RecentPerformance from "@/components/Student/charts/RecentPerformance.vue";
import MonthlyProgress from "@/components/Student/charts/MonthlyProgress.vue";
import StrengthWeakness from "@/components/Student/charts/StrengthWeakness.vue";
import ActivityHeatmap from "@/components/Student/charts/ActivityHeatmap.vue";

const API_URL = import.meta.env.VITE_API_URL;
const isLoading = ref(true);
const chartData = ref(null);

const { addCursorState, removeCursorState } = useCursor();

// Computed properties for quick stats
const totalQuizzes = computed(() => {
  if (!chartData.value?.recent_performance) return 0;
  return chartData.value.recent_performance.scores.length;
});

const averageScore = computed(() => {
  if (!chartData.value?.monthly_progress) return 0;
  const scores = chartData.value.monthly_progress.averageScores;
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
});

const currentStreak = computed(() => {
  if (!chartData.value?.heatmap) return 0;
  // Calculate streak from heatmap data
  let streak = 0;
  const today = new Date();
  const data = chartData.value.heatmap.data;
  // Implementation of streak calculation
  return streak;
});

const fetchChartData = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Token not found");

    const response = await axios.get(`${API_URL}/student/charts`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    chartData.value = response.data;
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchChartData();
});
</script>
