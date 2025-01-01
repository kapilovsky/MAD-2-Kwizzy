<script setup>
import { onMounted, onUnmounted } from "vue";
import { RouterLink } from "vue-router";
import Lenis from "lenis";
import batman from "../assets/images/landing-page/batman logo.jpg";
import dc from "../assets/images/landing-page/dc logo.png";
import superman from "../assets/images/landing-page/superman logo.png";
import Features from "@/components/LandingPage/Features.vue";
import Product from "@/components/LandingPage/ProductShowcase.vue";
import FAQs from "@/components/LandingPage/FAQs.vue";
import Testimonials from "@/components/LandingPage/Testimonials.vue";
import Pricing from "@/components/LandingPage/Pricing.vue";
import Footer from "@/components/LandingPage/Footer.vue";
import logo from "@/assets/images/landing-page/logo.png";

onMounted(() => {
  const lenis = new Lenis({
    duration: 1.2,
    smooth: true,
    axis: "vertical",
    direction: "vertical",
    gestureDirection: "vertical",
    gesture: true,
    scrollDirection: "vertical",
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }

  requestAnimationFrame(raf);

  onUnmounted(() => {
    lenis.destroy();
  });
});

import { ref } from "vue";

const sections = [
  { name: "Features", id: "features" },
  { name: "Product", id: "product" },
  { name: "Pricing", id: "pricing" },
  { name: "Testimonials", id: "testimonials" },
  { name: "FAQs", id: "faqs" },
];

const activeSection = ref("");

const handleScroll = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    const offset = element.offsetTop - 20;
    window.scrollTo({
      top: offset,
      behavior: "smooth",
    });
    activeSection.value = sectionId;
  }
};
</script>

<template>
  <main class="max-w-full mx-auto">
    <div class="container">
      <div>
        <div class="py-2 text-center banner">
          <div class="container">
            <p class="font-medium flex justify-center items-center gap-2">
              <span class="hidden sm:inline">
                Ready to ace your exams? Dive into Kwizzy – your ultimate quiz
                companion!
              </span>
              <a
                href="#"
                class="font-bold text-black underline underline-offset-4 flex items-center justify-center"
              >
                Start Your Journey Now
                <ion-icon name="arrow-forward-sharp"></ion-icon>
              </a>
            </p>
          </div>
        </div>
      </div>
      <div class="bg-black">
        <div class="px-4">
          <div class="flex items-center justify-between py-1">
            <div class="relative">
              <div>
                <img
                  :src="logo"
                  alt="logo"
                  class="rounded-full w-[5rem] mix-blend-exclusion"
                />
              </div>
            </div>
            <div
              class="flex items-center justify-between w-10 h-10 cursor-pointer sm:hidden hamburger"
            >
              <ion-icon name="menu-sharp"></ion-icon>
            </div>
            <nav class="items-center hidden gap-6 sm:flex">
              <button
                v-for="section in sections"
                :key="section.id"
                @click="handleScroll(section.id)"
                class="text-white transition cursor-pointer text-opacity-60 hover:text-opacity-100"
              >
                {{ section.name }}
              </button>
              <RouterLink to="/login">
                <button
                  class="px-4 py-2 font-medium text-black bg-white rounded-lg"
                >
                  Log In
                </button>
              </RouterLink>
              <RouterLink to="/signup">
                <button
                  class="px-4 py-2 font-medium text-black bg-white rounded-lg"
                >
                  Sign Up
                </button>
              </RouterLink>
            </nav>
          </div>
        </div>
      </div>
      <div
        class="text-white bg-black py-[72px] sm:py-24 relative overflow-clip hero"
      >
        <div
          class="absolute h-[375px] w-[750px] rounded-[100%] bg-black left-1/2 -translate-x-1/2 border-[#b48cde] top-[calc(100%-96px)] sm:w-[3000px] sm:h-[720px] sm:top-[calc(100%-120px)] ellipse"
        ></div>
        <div class="container relative">
          <div class="flex items-center justify-center">
            <a
              href="#"
              class="inline-flex gap-4 px-2 py-1 border rounded-lg border-white/70"
            >
              <span class="rainbow-text animated-gradient">
                Because Traditional Studying is so 2010
              </span>
              <!-- <span class="inline-flex items-center gap-1">
            Read More <ion-icon name="arrow-forward-sharp"></ion-icon>
          </span> -->
            </a>
          </div>
          <div class="hero-content">
            <h1 class="mt-6 font-bold text-center sm:text-[120px] text-7xl">
              Prep Smart<br />Stand Apart
            </h1>
            <p class="mt-8 text-lg text-center">
              From conquering chapters to crushing quizzes, we’ve got you
              covered.
              <br />
              Perfect for students, procrastinators, and that one overachiever
              in your class.
            </p>
          </div>

          <div class="flex justify-center mt-8">
            <button
              class="px-4 py-2 font-medium text-black bg-white rounded-lg"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
      <div class="text-white bg-black py-[20px]">
        <div class="container trusted-by">
          <h2 class="text-xl text-center">Trusted By</h2>
          <div class="flex flex-wrap items-center justify-center gap-16 images">
            <img class="w-[150px]" :src="batman" alt="batman logo" />
            <img class="w-[80px]" :src="dc" alt="dc logo" />
            <img class="w-[150px]" :src="superman" alt="superman logo" />
          </div>
        </div>
      </div>
      <Features />
      <Product />
      <Pricing />
      <Testimonials />
      <FAQs />
      <div
        id="call-to-action"
        class="call-to-action py-[72px] text-white text-center"
      >
        <div class="container">
          <h2 class="text-4xl font-bold">Ready to Crush Quizzes Like a Pro?</h2>
          <p class="mt-4 text-lg">
            Dive into Kwizzy – your ultimate quiz companion! <br />
            <span class="text-white/70 text-sm"
              >You’ve made it this far, so you clearly like us. Why not see what
              all the fuss is about?</span
            >
          </p>

          <div class="mt-8">
            <RouterLink to="/dashboard">
              <button class="px-4 py-2 bg-white text-black rounded-lg">
                Start Your Journey Now
              </button>
            </RouterLink>
          </div>
        </div>
      </div>
      <div
        class="text-white bg-black py-[72px] sm:py-24 relative overflow-clip footer-hero"
      >
        <div
          class="absolute h-[375px] w-[750px] rounded-[100%] bg-black left-1/2 -translate-x-1/2 border-[#000000] top-[calc(100%-96px)] sm:w-[3000px] sm:h-[720px] sm:top-[calc(100%-180px)] footer-ellipse"
        ></div>
      </div>
      <Footer />
    </div>
  </main>
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

.banner {
  background: linear-gradient(
    to right,
    rgba(250, 174, 255, 0.7),
    rgba(29, 213, 254, 0.7),
    rgba(255, 251, 35, 0.7),
    rgba(161, 153, 247, 0.7),
    rgb(252, 214, 255, 0.7)
  );
}

ion-icon {
  /* margin-top: 2px; */
  font-size: 20px;
  opacity: 0;
  transform: translateX(2px);
  transition: all 0.3s ease;
}

a:hover ion-icon {
  opacity: 1;
  transform: translateX(8px);
}

.hamburger ion-icon {
  color: white;
  font-size: 2rem;
}

.rainbow-text {
  background-image: linear-gradient(
    to right,
    #857aff,
    #52dfff,
    #fffc55,
    #92ff6a,
    #52dfff,
    #857aff
  );
  background-size: 300%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: Golos Text;
  /* font-weight: 600; */
  padding: 0px 8px;
}

.animated-gradient {
  animation: move-gradient 3s linear infinite;
}

@keyframes move-gradient {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 300% 50%;
  }
}

.hero-content h1 {
  font-family: Golos Text;
  letter-spacing: -6px;
}

.hero {
  background: linear-gradient(
    to bottom,
    #000,
    #2e3500 34%,
    #7f9204 65%,
    #ddff00 82%
  );
  background-size: 100% 110%;
  animation: gradientScroll 10s ease infinite;
}

.footer-hero {
  background: linear-gradient(
    to bottom,
    #000,
    #2f006f 34%,
    #41029a 65%,
    #4a00b0 82%
  );
  background-size: 100% 110%;
  animation: gradientScroll 10s ease infinite;
}

.call-to-action {
  background: linear-gradient(to bottom, #21034d 0%, #000000 100%);
}

@keyframes gradientScroll {
  0% {
    background-position: 0% 0%;
  }
  20% {
    background-position: 0% 80%;
  }
  70% {
    background-position: 0% 100%;
  }
  100% {
    background-position: 0% 0%;
  }
}

.ellipse {
  background: radial-gradient(closest-side, #000 82%, #ddff00);
}

.footer-ellipse {
  background: radial-gradient(closest-side, #000 82%, #350080);
}

.trusted-by h2 {
  font-family: "Instrument Serif";
  font-style: italic;
  font-weight: 400;
  color: white;
  opacity: 70%;
}

.images {
  margin-top: 32px;
  padding-bottom: 58px;
  position: relative;
}

.images::before {
  content: "";
  position: absolute;
  height: 100%;
  width: 80px;
  background: linear-gradient(to right, #000, #0000);
  left: 30%;
  top: 0;
  z-index: 20;
}

.images::after {
  content: "";
  position: absolute;
  height: 100%;
  width: 80px;
  background: linear-gradient(to left, #000, #0000);
  right: 34%;
  top: 0;
}

.images img {
  /* width: 150px; */
  filter: grayscale(100%);
  transition: all 0.7s ease;
  opacity: 70%;
}

.images img:hover {
  filter: grayscale(0%);
}

@media (max-width: 768px) {
  .images img {
    width: 80px;
  }

  .images::before {
    left: 15%;
  }

  .images::after {
    right: 15%;
  }
}
</style>
