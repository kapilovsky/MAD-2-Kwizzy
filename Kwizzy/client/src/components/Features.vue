<script setup>
import Feature from "./Feature.vue";
import { useMotion } from "@vueuse/motion";
// Data for features
const features = [
  {
    emoji: "📚",
    title: "Multi-Course Magic",
    description:
      "Jump between subjects like a academic ninja. Physics to Literature? We've got you covered. Just don't try them simultaneously - we're not responsible for brain explosions.",
  },
  {
    emoji: "👩‍🏫",
    title: "Admin Superpowers",
    description:
      "Teachers get their own superhero dashboard. Create quizzes, track progress, and resist the urge to make all answers 'C' just to mess with students.",
  },
  {
    emoji: "📉",
    title: "Progress Tracking",
    description:
      "Watch your knowledge grow with fancy charts and graphs. It's like a fitness tracker for your brain, minus the guilt-tripping notifications.",
  },
];
</script>

<template>
  <div id="features" class="text-white bg-black py-[72px] sm:py-24">
    <div class="container">
      <h2
        class="text-5xl font-bold tracking-tighter text-center sm:text-4xl"
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
        }"
        :focused="{
          scale: 1.1,
        }"
        :delay="200"
        :duration="500"
      >
        Supercharge Your Study Sessions ⚡
      </h2>
      <div class="max-w-xl mx-auto">
        <p
          class="mt-5 text-xl text-center text-white/70"
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
          }"
          :focused="{
            scale: 1.1,
          }"
          :delay="200"
          :duration="500"
        >
          Powerful enough for serious studying, fun enough to keep you awake.
          Here's how Kwizzy turns exam preparation from a chore into a choice.
        </p>
      </div>
      <div class="flex flex-col gap-4 mt-16 sm:flex-row px-10">
        <Feature
          v-for="feature in features"
          :key="feature.title"
          :emoji="feature.emoji"
          :title="feature.title"
          :description="feature.description"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add any custom styles for the Features section here */
</style>
