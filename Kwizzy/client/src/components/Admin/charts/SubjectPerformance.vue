<!-- components/charts/SubjectPerformanceChart.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4 sohne-mono">Subject Performance</h3>
    <div class="h-[400px]">
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
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
      type: "bar",
      label: "Average Score",
      data: props.data.averageScores,
      backgroundColor: "rgb(255, 235, 0,0.2)",
      borderColor: "rgb(255, 235, 0)",
      borderWidth: 1,
      borderRadius: 5,
      yAxisID: "y",
    },
    {
      type: "line",
      label: "Student Count",
      data: props.data.studentCounts,
      borderColor: "rgb(59, 130, 246)",
      backgroundColor: "rgba(59, 130, 246, 0.5)",
      borderWidth: 2,
      pointStyle: "circle",
      pointRadius: 6,
      pointHoverRadius: 8,
      yAxisID: "y1",
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: "index",
    intersect: false,
  },
  plugins: {
    legend: {
      position: "top",
      labels: {
        font: {
          family: "'IBM Plex Mono', monospace",
          size: 12,
        },
        usePointStyle: true,
        padding: 20,
      },
    },
    tooltip: {
      mode: "index",
      intersect: false,
      padding: 12,
      backgroundColor: "rgba(0, 0, 0, 0.8)",
      titleFont: {
        size: 14,
        family: "'IBM Plex Mono', monospace",
      },
      bodyFont: {
        size: 12,
        family: "'IBM Plex Mono', monospace",
      },
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || "";
          let value = context.parsed.y;

          if (label === "Average Score") {
            return `${label}: ${value.toFixed(1)}%`;
          }
          return `${label}: ${value} students`;
        },
      },
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        font: {
          family: "'IBM Plex Mono', monospace",
        },
      },
    },
    y: {
      type: "linear",
      display: true,
      position: "left",
      min: 0,
      max: 100,
      ticks: {
        callback: (value) => `${value}%`,
        font: {
          family: "'IBM Plex Mono', monospace",
        },
      },
      grid: {
        color: "rgba(0, 0, 0, 0.1)",
      },
      title: {
        display: true,
        text: "Average Score",
        font: {
          family: "'IBM Plex Mono', monospace",
        },
      },
    },
    y1: {
      type: "linear",
      display: true,
      position: "right",
      min: 0,
      grid: {
        drawOnChartArea: false,
      },
      ticks: {
        callback: (value) => `${value} students`,
        font: {
          family: "'IBM Plex Mono', monospace",
        },
      },
      title: {
        display: true,
        text: "Number of Students",
        font: {
          family: "'IBM Plex Mono', monospace",
        },
      },
    },
  },
};
</script>

<style scoped>
.sohne-mono {
  font-family: sohne-mono;
  text-transform: uppercase;
}
</style>
