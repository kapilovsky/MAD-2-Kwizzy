<!-- components/Student/charts/ActivityHeatmap.vue -->
<template>
  <div class="heatmap-container">
    <CalendarHeatmap
      :values="data.data"
      :end-date="data.endDate"
      :range-color="['#ebedf0', '#ffa07a', '#ff6b6b', '#dc143c', '#8b0000']"
    />
  </div>
</template>

<script setup>
import CalendarHeatmap from "vue-calendar-heatmap";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.heatmap-container {
  width: 100%;
  height: 200px;
}
</style>
