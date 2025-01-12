<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useScroll } from "@vueuse/core";
import { useMotion } from "@vueuse/motion";
import AppScreenshot from "../../assets/images/landing-page/app.png";

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

const normalizedProgress = computed(() => {
  return Math.min(scrollProgress.value / 0.6, 1);
});

// Watch for scroll changes
watch(scrollProgress, () => {
  console.log(scrollProgress.value);
});

const rotateXValue = computed(() => {
  return 15 - normalizedProgress.value * 15; // Will be 0 at 0.6 scroll progress
});

const opacityValue = computed(() => {
  return 0.35 + normalizedProgress.value * 0.65; // Will be 1 at 0.6 scroll progress
});

const scaleValue = computed(() => {
  return 0.95 + normalizedProgress.value * 0.05; // Subtle scale effect
});

const translateYValue = computed(() => {
  return 50 - normalizedProgress.value * 50; // Subtle float effect
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
    class="text-white bg-black py-[72px] sm:py-[132px] bg-gradient-to-b from-black to-[#000000] overflow-hidden"
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
          transform: `
            perspective(1000px) 
            rotateX(${rotateXValue}deg)
            scale(${scaleValue})
            translateY(${translateYValue}px)
          `,
          transition: 'all 0.3s ease-out',
        }"
      >
        <!-- Main Image -->
        <img
          class="rounded-xl w-[95vw] mx-auto relative z-10"
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
  filter: drop-shadow(0 30px 40px rgba(153, 0, 255, 0.4));
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

/* Add animation for floating elements */
@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.floating {
  animation: float 3s ease-in-out infinite;
}
</style>
