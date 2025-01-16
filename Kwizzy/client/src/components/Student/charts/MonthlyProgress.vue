<!-- components/Student/charts/MonthlyProgress.vue -->
<template>
  <div class="bg-white rounded-xl sm:p-6">
    <h3 class="sm:text-xl mb-4 arame">{{ data.title }}</h3>
    <div v-if="!hasData" class="text-center text-gray-500 py-10">
      No performance data available yet
    </div>
    <div v-else>
      <!-- Performance Stats -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="text-center p-4 bg-purple-50 rounded-lg">
          <div class="text-sm text-gray-600">Average Score</div>
          <div class="text-2xl font-bold text-purple-600">
            {{ currentAverageScore }}%
          </div>
        </div>
        <div class="text-center p-4 bg-green-50 rounded-lg">
          <div class="text-sm text-gray-600">Highest Score</div>
          <div class="text-2xl font-bold text-green-600">
            {{ currentHighestScore }}%
          </div>
        </div>
        <div class="text-center p-4 bg-blue-50 rounded-lg">
          <div class="text-sm text-gray-600">Total Quizzes</div>
          <div class="text-2xl font-bold text-blue-600">
            {{ totalQuizzes }}
          </div>
        </div>
      </div>

      <!-- Chart -->
      <div class="w-auto h-[300px]">
        <Line :data="chartData" :options="chartOptions" />
      </div>

      <!-- Legend -->
      <div class="mt-4 flex flex-wrap justify-center gap-4 text-sm">
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
          <span>Average Score</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 bg-green-500 rounded-full"></div>
          <span>Highest Score</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 bg-red-500 rounded-full"></div>
          <span>Lowest Score</span>
        </div>
      </div>
    </div>
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
  Filler,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const hasData = computed(() => {
  return props.data.labels && props.data.labels.length > 0;
});

const currentAverageScore = computed(() => {
  const scores = props.data.averageScores;
  return scores.length ? Math.round(scores[scores.length - 1]) : 0;
});

const currentHighestScore = computed(() => {
  const scores = props.data.highestScores;
  return scores.length ? Math.round(scores[scores.length - 1]) : 0;
});

const totalQuizzes = computed(() => {
  return props.data.quizCount.reduce((a, b) => a + b, 0);
});

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      label: "Average Score",
      data: props.data.averageScores,
      borderColor: "rgb(147, 51, 234)",
      backgroundColor: "rgba(255, 255, 255, 0.1)",
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 4,
      //   pointBackgroundColor: "rgb(147, 51, 234)",
    },
    {
      label: "Highest Score",
      data: props.data.highestScores,
      borderColor: "rgb(34, 197, 94)",
      backgroundColor: "rgba(255, 255, 255, 0.1)",
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 4,
      // pointBackgroundColor: "rgb(34, 197, 94)",
    },
    {
      label: "Lowest Score",
      data: props.data.lowestScores,
      borderColor: "rgb(239, 68, 68)",
      backgroundColor: "rgba(255, 255, 255, 0.1)",
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 4,
      //   pointBackgroundColor: "rgb(239, 68, 68)",
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      mode: "index",
      intersect: false,
      backgroundColor: "rgba(0, 0, 0, 0.8)",
      padding: 12,
      titleFont: {
        size: 14,
      },
      bodyFont: {
        size: 13,
      },
      callbacks: {
        label: function (context) {
          return `${context.dataset.label}: ${Math.round(context.raw)}%`;
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      grid: {
        color: "rgba(0, 0, 0, 0.05)",
      },
      ticks: {
        callback: (value) => `${value}%`,
        font: {
          size: 12,
        },
      },
    },
    x: {
      grid: {
        display: false,
      },
      ticks: {
        font: {
          size: 12,
        },
      },
    },
  },
  interaction: {
    intersect: false,
    mode: "index",
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
}
</style>
