<script setup>
import Feature from "./Feature.vue";
const features = [
  {
    emoji: "📚",
    title: "Multi-Course Magic",
    description:
      "Jump between subjects like a academic ninja. Physics to Literature? I've got you covered. Just don't try them simultaneously - I am not responsible for brain explosions.",
  },
  {
    emoji: "👩‍🏫",
    title: "Admin Superpowers",
    description:
      "Admin gets their own dashboard. Create quizzes, track progress, and resist the urge to make all answers 'C' just to mess with students.",
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
    <div class="container relative overflow-hidden">
      <h2
        class="text-5xl font-bold tracking-tighter text-center sm:text-4xl"
        v-motion
        :visible-once="{
          opacity: 1,
          y: 0,
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
          :visible-once="{
            opacity: 1,
            y: 0,
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
      <div
        class="absolute -rotate-[50deg] w-[250px] h-[400px] left-16 bottom-0 bg-[#ddff0061] blur-[75px] rounded-[400px] pointer-events-none"
      ></div>
      <div
        class="absolute rotate-[50deg] w-[250px] h-[400px] right-16 bottom-0 bg-[#ddff0061] blur-[75px] rounded-[400px] pointer-events-none"
      ></div>
      <div class="flex flex-col gap-4 mt-16 sm:flex-row px-10 z-10 static">
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
