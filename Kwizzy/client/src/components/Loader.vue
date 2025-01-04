<!-- components/UI/SkeletonLoader.vue -->
<script setup>
defineProps({
  count: {
    type: Number,
    default: 4,
  },
});
</script>

<template>
  <div class="skeleton-wrapper">
    <div class="lds-hourglass"></div>
  </div>
</template>

<style scoped>
.skeleton-wrapper {
  position: absolute;
  z-index: 999;
  left: calc(50% - 40px);
  top: calc(40% - 40px);
}

.lds-hourglass,
.lds-hourglass:after {
  box-sizing: border-box;
}
.lds-hourglass {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
  /* color: white; */
}
.lds-hourglass:after {
  content: " ";
  display: block;
  border-radius: 50%;
  width: 0;
  height: 0;
  margin: 8px;
  box-sizing: border-box;
  border: 32px solid currentColor;
  border-color: currentColor transparent currentColor transparent;
  animation: lds-hourglass 1.2s infinite;
}
@keyframes lds-hourglass {
  0% {
    transform: rotate(0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }
  50% {
    transform: rotate(900deg);
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }
  100% {
    transform: rotate(1800deg);
  }
}
</style>
