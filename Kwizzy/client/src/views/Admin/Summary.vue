<!-- views/Admin/Dashboard.vue -->
<template>
  <Loader v-if="isLoading" />

  <Sidebar v-else>
    <div class="p-6">
      <h2 class="text-2xl font-bold mb-6">Dashboard Overview</h2>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-xl p-6">
          <h3 class="text-sm text-gray-500 uppercase">Total Students</h3>
          <p class="text-3xl font-bold">{{ total_students }}</p>
        </div>
        <!-- Add more stat cards -->
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PerformanceDistribution :data="performance_distribution" />

        <QualificationChart :data="qualification_distribution" />

        <ActivityChart :data="activity" />

        <SubjectPerformance :data="subject_performance" />
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import Sidebar from "@/components/Admin/Sidebar.vue";
import ActivityChart from "@/components/Admin/charts/ActivityChart.vue";
import QualificationChart from "@/components/Admin/charts/QualificationChart.vue";
import SubjectPerformance from "@/components/Admin/charts/SubjectPerformance.vue";
import PerformanceDistribution from "@/components/Admin/charts/PerformanceDistribution.vue";

const activity = ref(null);
const statistics = ref(null);
const total_students = ref(null);
const subject_performance = ref(null);
const performance_distribution = ref(null);
const qualification_distribution = ref(null);
const API_URL = import.meta.env.VITE_API_URL;
const isLoading = ref(true);

const fetchStatistics = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("Token not found");
    }
    const response = await axios.get(`${API_URL}/charts`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    statistics.value = response.data;
    performance_distribution.value = response.data.performance;
    activity.value = response.data.activity;
    qualification_distribution.value = response.data.qualifications;
    subject_performance.value = response.data.subjects;
    console.log("stats", statistics.value);
    total_students.value = activity.value.data.reduce(
      (acc, curr) => acc + curr,
      0
    );
  } catch (error) {
    console.error("Error fetching statistics:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStatistics();
});
</script>
