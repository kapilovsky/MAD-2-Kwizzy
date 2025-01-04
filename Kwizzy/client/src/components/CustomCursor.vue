<!-- components/CustomCursor.vue -->
<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const cursorDot = ref(null);
const cursorOutline = ref(null);
const isClicking = ref(false);
const cursorVisible = ref(false);
const cursorScaled = ref(false);

const endX = ref(window.innerWidth / 2);
const endY = ref(window.innerHeight / 2);
const _x = ref(0);
const _y = ref(0);
const requestRef = ref(null);

const toggleCursorVisibility = () => {
  if (cursorVisible.value) {
    cursorDot.value.style.opacity = 1;
    cursorOutline.value.style.opacity = 1;
  } else {
    cursorDot.value.style.opacity = 0;
    cursorOutline.value.style.opacity = 0;
  }
};

const mouseOverEvent = () => {
  cursorScaled.value = true;
  cursorDot.value.classList.add("hovering");
  cursorOutline.value.classList.add("hovering");
};

const mouseOutEvent = () => {
  cursorScaled.value = false;
  cursorDot.value.classList.remove("hovering");
  cursorOutline.value.classList.remove("hovering");
};

const mouseEnterEvent = () => {
  cursorVisible.value = true;
  toggleCursorVisibility();
};

const mouseLeaveEvent = () => {
  cursorVisible.value = false;
  toggleCursorVisibility();
};

const mouseMoveEvent = (e) => {
  cursorVisible.value = true;
  toggleCursorVisibility();

  endX.value = e.clientX;
  endY.value = e.clientY;

  cursorDot.value.style.top = endY.value + "px";
  cursorDot.value.style.left = endX.value + "px";
};

const animateOutline = () => {
  _x.value += (endX.value - _x.value) / 8;
  _y.value += (endY.value - _y.value) / 8;
  cursorOutline.value.style.top = _y.value + "px";
  cursorOutline.value.style.left = _x.value + "px";

  requestRef.value = requestAnimationFrame(animateOutline);
};

const mouseDownEvent = () => {
  isClicking.value = true;
  cursorDot.value.classList.add("clicking");
  cursorOutline.value.classList.add("clicking");
};

const mouseUpEvent = () => {
  isClicking.value = false;
  cursorDot.value.classList.remove("clicking");
  cursorOutline.value.classList.remove("clicking");
};

onMounted(() => {
  document.addEventListener("mousemove", mouseMoveEvent);
  document.addEventListener("mouseenter", mouseEnterEvent);
  document.addEventListener("mouseleave", mouseLeaveEvent);
  document.addEventListener("mousedown", mouseDownEvent);
  document.addEventListener("mouseup", mouseUpEvent);

  // Add hover effect to all clickable elements
  const clickables = document.querySelectorAll(
    'a, button, input[type="submit"], input[type="button"], .clickable'
  );

  clickables.forEach((el) => {
    el.addEventListener("mouseover", mouseOverEvent);
    el.addEventListener("mouseout", mouseOutEvent);
  });

  requestRef.value = requestAnimationFrame(animateOutline);
});

onUnmounted(() => {
  document.removeEventListener("mousemove", mouseMoveEvent);
  document.removeEventListener("mouseenter", mouseEnterEvent);
  document.removeEventListener("mouseleave", mouseLeaveEvent);
  document.removeEventListener("mousedown", mouseDownEvent);
  document.removeEventListener("mouseup", mouseUpEvent);

  const clickables = document.querySelectorAll(
    'a, button, input[type="submit"], input[type="button"], .clickable'
  );

  clickables.forEach((el) => {
    el.removeEventListener("mouseover", mouseOverEvent);
    el.removeEventListener("mouseout", mouseOutEvent);
  });

  cancelAnimationFrame(requestRef.value);
});
</script>

<template>
  <div class="cursor-wrapper">
    <div ref="cursorOutline" class="cursor-outline"></div>
    <div ref="cursorDot" class="cursor-dot"></div>
  </div>
</template>

<style scoped>
.cursor-wrapper {
  pointer-events: none;
}

.magnetic {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.cursor-dot {
  width: 10px;
  height: 10px;
  background-color: rgb(255, 255, 255);
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
  z-index: 999;
  mix-blend-mode: difference;
}

.cursor-outline {
  width: 30px;
  height: 30px;
  border: 2px solid rgb(255, 255, 255);
  mix-blend-mode: difference;
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
  z-index: 998;
}

/* Optional: Add different states for the cursor */
.cursor-dot.clicking {
  transform: translate(-50%, -50%) scale(0.8);
}

.cursor-outline.clicking {
  transform: translate(-50%, -50%) scale(1.5);
}

.cursor-dot.hovering {
  transform: translate(-50%, -50%) scale(1.75);
}

.cursor-outline.hovering {
  transform: translate(-50%, -50%) scale(1.5);
}
</style>
