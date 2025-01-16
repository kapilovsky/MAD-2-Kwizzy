<template>
  <div class="heatmap-container">
    <div v-if="debug" class="mb-4 p-2 bg-gray-100 rounded">
      <pre>{{ JSON.stringify(props.data, null, 2) }}</pre>
    </div>

    <div v-if="!isDataValid" class="text-center text-gray-500">
      No activity data available
    </div>
    <div v-else>
      <CalendarHeatmap
        :values="formattedData"
        :end-date="endDate"
        :range-color="[
          '#f0f6ff',
          '#e3eeff',
          '#d6e6ff',
          '#c9ddff',
          '#b1d0ff',
          '#99c4ff',
          '#82b7ff',
          '#6aabff',
          '#529eff',
          '#3b91ff',
          '#2484ff',
          '#0d77ff',
          '#0066ff',
          '#0052cc',
          '#003d99',
          '#002966',
          '#001f4d',
          '#001433',
          '#000a1a',
          '#000510',
        ]"
        :tooltip="true"
        :tooltip-unit="'quiz'"
        :max="Math.max(...formattedData.map((item) => item.count)) + 1"
        :round="2"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { CalendarHeatmap } from "vue3-calendar-heatmap";

const debug = ref(false); // Set to false in production

const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({
      data: [],
      endDate: new Date().toISOString(),
    }),
  },
});

const isDataValid = computed(() => {
  return (
    props.data?.data &&
    Array.isArray(props.data.data) &&
    props.data.data.length > 0
  );
});

const endDate = computed(() => {
  return props.data?.endDate || new Date().toISOString().split("T")[0];
});

const formattedData = computed(() => {
  if (!isDataValid.value) return [];

  return props.data.data.map((item) => ({
    date: item.date,
    count: parseInt(item.count),
  }));
});
</script>

<style scoped>
.heatmap-container {
  width: 70%;
  min-height: 300px;
  padding: 1rem;
  margin: 0 auto;
}

/* Custom styles for the heatmap */
:deep(.vch__container) {
  color: inherit;
}

:deep(.vch__legend) {
  margin-top: 1rem;
  font-size: 0.5rem;
  color: rgb(94, 94, 94);
}

:deep(.vch__day__label) {
  font-size: 0.6rem;
}

:deep(.vch__month__label) {
  font-size: 0.6rem;
}

:deep(.vch__external-legend-wrapper) {
  padding: 2px;
}

@media (max-width: 768px) {
  .heatmap-container {
    width: 100%;
    padding: 0;
    min-height: 120px;
  }
}
</style>
