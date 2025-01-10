<!-- components/charts/PerformanceDistribution.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">Performance Distribution</h3>
    <div class="h-[400px] w-[400px]">
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const chartData = computed(() => {
  if (!props.data) return null;

  return {
    labels: props.data.labels,
    datasets: [
      {
        label: "Number of Students",
        data: props.data.data,
        backgroundColor: [
          "rgba(34, 197, 94, 0.5)", // green
          "rgba(59, 130, 246, 0.5)", // blue
          "rgba(234, 179, 8, 0.5)", // yellow
          "rgba(239, 68, 68, 0.5)", // red
        ],
        borderColor: [
          "rgb(34, 197, 94)",
          "rgb(59, 130, 246)",
          "rgb(234, 179, 8)",
          "rgb(239, 68, 68)",
        ],
        borderWidth: 1,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
      },
    },
  },
};

onMounted(() => {
  console.log("chartData", props.data);
});
</script>
