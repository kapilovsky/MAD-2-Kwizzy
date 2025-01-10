<!-- components/charts/QualificationChart.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">Qualification Distribution</h3>
    <Doughnut v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Doughnut } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const chartData = computed(() => ({
  labels: Object.keys(props.data),
  datasets: [
    {
      data: Object.values(props.data),
      backgroundColor: [
        "rgba(59, 130, 246, 0.5)",
        "rgba(34, 197, 94, 0.5)",
        "rgba(234, 179, 8, 0.5)",
        "rgba(239, 68, 68, 0.5)",
        "rgba(168, 85, 247, 0.5)",
      ],
      borderColor: [
        "rgb(59, 130, 246)",
        "rgb(34, 197, 94)",
        "rgb(234, 179, 8)",
        "rgb(239, 68, 68)",
        "rgb(168, 85, 247)",
      ],
      borderWidth: 1,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "right",
    },
  },
};
</script>
