<!-- views/Admin/Dashboard.vue -->
<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">Dashboard Overview</h2>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-xl p-6">
        <h3 class="text-sm text-gray-500 uppercase">Total Students</h3>
        <p class="text-3xl font-bold">{{ statistics.total_students }}</p>
      </div>
      <!-- Add more stat cards -->
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <PerformanceDistributionChart
        :data="statistics.performance_distribution"
      />

      <QualificationChart :data="statistics.qualification_distribution" />

      <ActivityChart
        :active-students="statistics.active_students"
        :inactive-students="statistics.inactive_students"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import PerformanceDistributionChart from "@/components/charts/PerformanceDistribution.vue";
import QualificationChart from "@/components/charts/QualificationChart.vue";
import ActivityChart from "@/components/charts/ActivityChart.vue";

const statistics = ref(null);

const fetchStatistics = async () => {
  try {
    const response = await axios.get(`${API_URL}/admin/statistics`);
    statistics.value = response.data;
  } catch (error) {
    console.error("Error fetching statistics:", error);
  }
};

onMounted(() => {
  fetchStatistics();
});
</script>
