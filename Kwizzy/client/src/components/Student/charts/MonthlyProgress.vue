<!-- components/Student/charts/MonthlyProgress.vue -->
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
      label: "Average Score",
      data: props.data.averageScores,
      fill: false,
      borderColor: "rgb(178, 8, 17)",
      tension: 0.1,
    },
    {
      label: "Quizzes Taken",
      data: props.data.quizCount,
      fill: false,
      borderColor: "rgb(75, 192, 192)",
      tension: 0.1,
      yAxisID: "quizCount",
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
      title: {
        display: true,
        text: "Score (%)",
      },
    },
    quizCount: {
      position: "right",
      beginAtZero: true,
      title: {
        display: true,
        text: "Number of Quizzes",
      },
    },
  },
};
</script>
