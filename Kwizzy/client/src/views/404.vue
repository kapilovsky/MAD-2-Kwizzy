<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
import logo from "../assets/images/landing-page/white logo.png";

const isNavigating = ref(false);

const handleKeyPress = async (e) => {
  if (e.key === "Escape") {
    isNavigating.value = true;
    try {
      await router.push({
        path: "/",
        replace: true,
      });
      window.location.reload();
    } catch (error) {
      console.log(error, "error");
    } finally {
      isNavigating.value = false;
    }
  }
};

onMounted(() => {
  document.addEventListener("keydown", handleKeyPress);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeyPress);
});
</script>

<template>
  <div class="w-full h-full bg-black">
    <div
      class="bg-[#0000dd] h-screen flex flex-col items-center gap-24 flicker"
    >
      <div class="flex flex-col justify-center items-center mt-[150px]">
        <div>
          <h1 class="text-4xl font-medium text-white chintzy">
            ERROR: 0x00000404 PAGE NOT FOUND
          </h1>

          <div>
            <p class="text-white arame-mono text-xl mt-4">
              The page you are looking for does not exist :(
            </p>
            <ul class="mt-10 space-y-4">
              <li class="text-white arame-mono text-xl">
                * You may have mistyped the URL.
              </li>
              <li class="text-white text-xl arame-mono">
                * Or the page may have moved.
              </li>

              <li class="text-white text-xl arame-mono">
                * Or the page may have deleted.
              </li>

              <li class="text-white text-xl arame-mono">
                * Or the page may have never existed.
              </li>
            </ul>
            <div class="text-white arame-mono text-sm mt-4">
              <p>Technical information:</p>
              <p>
                *** STOP: 0x00000404 (0x0000000000000000, 0xFFFFF80409C3F000)
              </p>
              <p>
                *** PAGE_NOT_FOUND.sys - Address 0xFFFFF80409C3F000 base at
                0xFFFFF80409C00000
              </p>
            </div>
            <div>
              <p
                class="text-white mix-blend-difference text-lg arame-mono mt-4"
              >
                Press [ESC] to return to the home page
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center items-center gap-2">
        <img :src="logo" class="w-[40px] h-[40px]" alt="" />
        <h1 class="text-xl font-bold text-white sohne">Kwizzy</h1>
      </div>
    </div>
  </div>
</template>

<style scoped>
@font-face {
  font-family: chintzy;
  src: url(../assets/fonts/chintzy.ttf);
}
@font-face {
  font-family: rixel;
  src: url(../assets/fonts/Rixel.ttf);
}

@font-face {
  font-family: arame-mono;
  src: url(../assets/fonts/ArameMono.ttf);
}

.txtart {
  font-family: "lucida grande", tahoma, verdana, arial, sans-serif;
  height: 800px;
  width: 600px;
  whitespace: pre;
}

textarea {
  whitespace: pre;
  height: 800px;
}

.chintzy {
  font-family: chintzy;
}

.rixel {
  font-family: rixel;
}

.arame-mono {
  font-family: arame-mono;
}

.flicker {
  animation: flicker 0.2s infinite;
}

.flicker::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.25) 0px,
    rgba(0, 0, 0, 0.25) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
}

@keyframes flicker {
  0% {
    opacity: 1;
  }
  10% {
    opacity: 0.7;
  }
  20% {
    opacity: 1;
  }
  30% {
    opacity: 0.84;
  }
  40% {
    opacity: 1;
  }
  50% {
    opacity: 0.85;
  }
  60% {
    opacity: 1;
  }
  70% {
    opacity: 0.9;
  }
  80% {
    opacity: 1;
  }
  90% {
    opacity: 0.92;
  }
  100% {
    opacity: 1;
  }
}
</style>
