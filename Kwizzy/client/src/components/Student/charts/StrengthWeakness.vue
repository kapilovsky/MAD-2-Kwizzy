<!-- components/Student/charts/StrengthWeakness.vue -->
<template>
  <div class="bg-white rounded-xl p-6">
    <h3 class="text-xl mb-4 arame">{{ data.title }}</h3>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <h4 class="text-sm font-semibold mb-2 text-green-600 sohne-mono">
          Strengths
        </h4>
        <ul class="space-y-2">
          <li
            v-for="strength in data.strengths"
            :key="strength.chapter"
            class="text-sm p-2 bg-green-50 rounded sohne"
          >
            {{ strength.chapter }} ({{ strength.score.toFixed(1) }}%)
          </li>
        </ul>
      </div>
      <div>
        <h4 class="text-sm sohne-mono font-semibold mb-2 text-red-600">
          Areas for Improvement
        </h4>
        <ul class="space-y-2">
          <li
            v-for="weakness in data.weaknesses"
            :key="weakness.chapter"
            class="text-sm p-2 bg-red-50 rounded sohne"
          >
            {{ weakness.chapter }} ({{ weakness.score.toFixed(1) }}%)
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>
