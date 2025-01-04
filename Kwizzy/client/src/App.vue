<script setup>
import { RouterLink, RouterView } from "vue-router";
import CustomCursor from "./components/CustomCursor.vue";
</script>

<template>
  <CustomCursor />
  <RouterView v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>
</template>

<style>
* {
  cursor: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
