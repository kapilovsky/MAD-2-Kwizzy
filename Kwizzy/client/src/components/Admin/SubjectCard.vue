<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const props = defineProps({
  subjects: {
    type: Array,
    required: true,
  },
});

const modalRef = ref(null);
</script>

<template>
  <div class="relative">
    <!-- Subject Grid -->
    <div
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <div
        v-for="subject in subjects"
        :key="subject.id"
        class="group cursor-pointer bg-[#fafafa] rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border-2 border-[#e5e7ebd6]"
      >
        <div class="relative">
          <img
            :src="subject.image"
            :alt="subject.name"
            class="w-full h-52 object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 group-hover:scale-105 transition-all duration-300"
          ></div>
        </div>

        <div class="p-3">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ subject.name }}
          </h3>
          <p class="mt-1 text-sm text-gray-600">
            {{ subject.description }}
          </p>

          <div class="mt-4 flex justify-between text-sm">
            <span class="text-gray-600"> {{ subject.students }} Students </span>
            <span class="text-gray-600">
              {{ subject.quiz_count }} Quizzes
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media (max-width: 640px) {
  .fixed.bottom-6.right-6 {
    bottom: 1rem;
    right: 1rem;
  }
}
</style>
