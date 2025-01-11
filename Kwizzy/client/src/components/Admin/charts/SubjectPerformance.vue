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
      borderWidth: 2,
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
      pointHoverRadius: 10,
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
          family: "'sohne'",
          size: 13,
        },
        usePointStyle: true,
        pointStyle: "circle",
        pointRadius: 4,
        pointHoverRadius: 10,
      },
    },
    tooltip: {
      mode: "index",
      intersect: false,
      padding: 12,
      backgroundColor: "rgba(0, 0, 0, 0.8)",
      titleFont: {
        size: 14,
        family: "sohne",
      },
      bodyFont: {
        size: 12,
        family: "sohne",
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
          family: "'sohne-mono', monospace",
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
          family: "'sohne-mono', monospace",
        },
      },
      grid: {
        color: "rgba(0, 0, 0, 0.1)",
      },
      title: {
        display: true,
        text: "Average Score",
        font: {
          family: "'sohne-mono', monospace",
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
          family: "'sohne-mono', monospace",
        },
      },
      title: {
        display: true,
        text: "Number of Students",
        font: {
          family: "'sohne-mono', monospace",
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
