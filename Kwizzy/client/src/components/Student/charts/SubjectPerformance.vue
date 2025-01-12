<!-- components/Student/charts/SubjectPerformance.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl mb-4 font-semibold">{{ data.title }}</h3>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
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
      label: "Average Score",
      data: props.data.averageScores,
      backgroundColor: "rgba(178, 8, 17, 0.5)",
      borderColor: "rgba(178, 8, 17, 1)",
      borderWidth: 1,
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
