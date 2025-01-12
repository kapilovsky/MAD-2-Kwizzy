<!-- views/StudentDashboard.vue -->
<template>
  <div class="p-2">
    <Loader v-if="isLoading" />
    <div v-else>
      <h2
        @mouseover="addCursorState('heading-hover')"
        @mouseout="removeCursorState('heading-hover')"
        class="sm:text-5xl text-3xl mb-6 sohne-mono font-bold w-fit"
      >
        SUMMARY 📒
      </h2>

      <!-- Activity Heatmap -->
      <div class="mt-6 bg-white rounded-xl p-6">
        <h3 class="text-xl mb-4 arame">Activity Calendar</h3>
        <ActivityHeatmap v-if="chartData?.heatmap" :data="chartData.heatmap" />
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SubjectPerformance :data="chartData.subject_performance" />
        <RecentPerformance :data="chartData.recent_performance" />
        <MonthlyProgress :data="chartData.monthly_progress" />
        <StrengthWeakness :data="chartData.strength_weakness" />
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

const fetchChartData = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Token not found");

    const response = await axios.get(`${API_URL}/student/charts`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    chartData.value = response.data;
    console.log("API Response:", response.data.monthly_progress);
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

<style>
.arame {
  font-family: "Arame";
}
</style>
