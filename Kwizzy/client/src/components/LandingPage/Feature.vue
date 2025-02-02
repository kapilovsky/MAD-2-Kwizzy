<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useMotion } from "@vueuse/motion";

// Props for the Feature component
defineProps(["emoji", "title", "description"]);

// Reactive state for mouse position and mask
const border = ref(null);
const offsetX = ref(-100);
const offsetY = ref(-100);

const maskImage = computed(
  () =>
    `radial-gradient(100px 100px at ${offsetX.value}px ${offsetY.value}px, black, transparent)`
);

const updateMousePosition = (e) => {
  const borderRect = border.value.getBoundingClientRect();
  offsetX.value = e.clientX - borderRect.x;
  offsetY.value = e.clientY - borderRect.y;
};

// Lifecycle hooks
onMounted(() => {
  window.addEventListener("mousemove", updateMousePosition);
});

onUnmounted(() => {
  window.removeEventListener("mousemove", updateMousePosition);
});
</script>

<template>
  <div
    class="relative px-5 py-10 text-center border-2 border-white/20 rounded-xl sm:flex-1 bg-black/60"
  >
    <div
      v-motion
      :initial="{
        opacity: 0,
        y: 50,
      }"
      :visible-once="{
        opacity: 1,
        y: 0,
      }"
      :leave="{
        y: -100,
        opacity: 0,
        transition: {
          duration: 1000,
        },
      }"
      :focused="{
        scale: 1.1,
      }"
      :delay="200"
      :duration="600"
      class="absolute inset-[-1px] border-2 border-[#ef0] rounded-xl"
      ref="border"
      :style="{ WebkitMaskImage: maskImage, maskImage: maskImage }"
    ></div>
    <h1
      v-motion
      :initial="{
        opacity: 0,
        y: 50,
      }"
      :visible-once="{
        opacity: 1,
        y: 0,
      }"
      :leave="{
        y: -100,
        opacity: 0,
        transition: {
          duration: 1000,
        },
      }"
      :focused="{
        scale: 1.1,
      }"
      :delay="200"
      :duration="600"
      class="text-5xl"
    >
      {{ emoji }}
    </h1>
    <h3
      v-motion
      :initial="{
        opacity: 0,
        y: 50,
      }"
      :visible-once="{
        opacity: 1,
        y: 0,
      }"
      :leave="{
        y: -100,
        opacity: 0,
        transition: {
          duration: 1000,
        },
      }"
      :focused="{
        scale: 1.1,
      }"
      :delay="200"
      :duration="600"
      class="mt-6 font-bold"
    >
      {{ title }}
    </h3>
    <p
      v-motion
      :initial="{
        opacity: 0,
        y: 50,
      }"
      :visible-once="{
        opacity: 1,
        y: 0,
      }"
      :leave="{
        y: -100,
        opacity: 0,
        transition: {
          duration: 1000,
        },
      }"
      :focused="{
        scale: 1.1,
      }"
      :delay="200"
      :duration="600"
      class="mt-2 text-white/70"
    >
      {{ description }}
    </p>
  </div>
</template>

<style scoped>
/* Add any custom styles for the Feature component here */
</style>
