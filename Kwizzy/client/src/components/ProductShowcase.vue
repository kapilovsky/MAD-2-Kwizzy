<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useScroll } from "@vueuse/core";
import { useMotion } from "@vueuse/motion";
import AppScreenshot from "../assets/images/landing-page/app.jpg";

const appScreenshot = ref(null);
const scrollProgress = ref(0);

// Scroll handler
const handleScroll = () => {
  if (!appScreenshot.value) return;

  const rect = appScreenshot.value.getBoundingClientRect();
  const scrollPercentage =
    1 - rect.bottom / (window.innerHeight + rect.height + 400);
  scrollProgress.value = Math.min(Math.max(scrollPercentage, 0), 1);
};

// Computed properties for transformations
const rotateXValue = computed(() => {
  return 14 - scrollProgress.value * 16;
});

const opacityValue = computed(() => {
  return 0.2 + scrollProgress.value * 0.8;
});

// Mount scroll listener
onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

// Clean up
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<template>
  <div
    id="product"
    class="text-white bg-black py-[72px] bg-gradient-to-b from-black to-[#000000] overflow-hidden"
  >
    <div class="container">
      <h2
        class="text-6xl font-bold tracking-tighter text-center"
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1 }"
        :delay="300"
      >
        Intuitive Dashboard
      </h2>
      <div class="max-w-xl mx-auto">
        <p
          class="mt-5 text-sm text-center text-white/70"
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0 }"
          :delay="500"
        >
          Like your favorite social media feed, but instead of 🐈 videos, you
          get smarter. Our dashboard keeps everything organized, from quizzes to
          progress reports - because your brain deserves better than scattered
          sticky notes
        </p>
      </div>
      <div
        ref="appScreenshot"
        class="mt-14 transform-gpu px-4 py-2 rounded-xl"
        :style="{
          opacity: opacityValue,
          transform: `perspective(1000px) rotateX(${rotateXValue}deg)`,
          transition: 'all 0.3s ease-out',
        }"
      >
        <img
          class="rounded-xl w-[90vw] mx-auto"
          :src="AppScreenshot"
          alt="The Product Screenshot"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.transform-gpu {
  will-change: transform, opacity;
  transform-style: preserve-3d;
  backface-visibility: hidden;
}

img {
  transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}

.container {
  max-width: 1800px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>
