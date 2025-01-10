<!-- components/charts/ActivityChart.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">Student Activity</h3>
    <Pie v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  activeStudents: Number,
  inactiveStudents: Number,
});

const chartData = computed(() => ({
  labels: ["Active Students", "Inactive Students"],
  datasets: [
    {
      data: [props.activeStudents, props.inactiveStudents],
      backgroundColor: ["rgba(34, 197, 94, 0.5)", "rgba(239, 68, 68, 0.5)"],
      borderColor: ["rgb(34, 197, 94)", "rgb(239, 68, 68)"],
      borderWidth: 1,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom",
    },
  },
};
</script>
