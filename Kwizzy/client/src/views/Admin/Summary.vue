<!-- views/Admin/Dashboard.vue -->
<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">Dashboard Overview</h2>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-xl p-6">
        <h3 class="text-sm text-gray-500 uppercase">Total Students</h3>
        <!-- <p class="text-3xl font-bold">{{ total_students }}</p> -->
      </div>
      <!-- Add more stat cards -->
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- <PerformanceDistribution :data="performance_distribution" />

      <QualificationChart :data="qualification_distribution" />

      <ActivityChart
        :active-students="active_students"
        :inactive-students="inactive_students"
      /> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import PerformanceDistribution from "@/components/Admin/charts/PerformanceDistribution.vue";
import QualificationChart from "@/components/Admin/charts/QualificationChart.vue";
import ActivityChart from "@/components/Admin/charts/ActivityChart.vue";

const statistics = ref(null);
const performance_distribution = ref(null);
const qualification_distribution = ref(null);
const active_students = ref(null);
const inactive_students = ref(null);
const total_students = ref(null);

const API_URL = import.meta.env.VITE_API_URL;

const fetchStatistics = async () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      throw new Error("Token not found");
    }
    const response = await axios.get(`${API_URL}/charts`);
    statistics.value = response.data;
    console.log("statistics", statistics.value);
  } catch (error) {
    console.error("Error fetching statistics:", error);
  }
};

onMounted(() => {
  fetchStatistics();
});
</script>
