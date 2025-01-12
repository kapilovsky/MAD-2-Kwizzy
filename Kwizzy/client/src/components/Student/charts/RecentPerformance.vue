<!-- components/Student/charts/RecentPerformance.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl mb-4 font-semibold">{{ data.title }}</h3>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      label: "Score",
      data: props.data.scores,
      fill: false,
      borderColor: "rgb(178, 8, 17)",
      tension: 0.1,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
    },
  },
};
</script>
