<script setup>
import batman from "../assets/images/landing-page/batman logo.jpg";
import dc from "../assets/images/landing-page/dc logo.png";
import superman from "../assets/images/landing-page/superman logo.png";
import Features from "../components/Features.vue";
import Product from "../components/ProductShowcase.vue";
import FAQs from "../components/FAQs.vue";
</script>

<template>
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
            class="font-medium text-black underline underline-offset-4 flex items-center gap-1 justify-center"
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
            <!-- <img
              src="{logo}"
              alt="logo"
              class="rounded-full w-[5rem] mix-blend-exclusion"
            /> -->
          </div>
        </div>
        <div
          class="flex items-center justify-between w-10 h-10 cursor-pointer sm:hidden hamburger"
        >
          <ion-icon name="menu-sharp"></ion-icon>
        </div>
        <nav class="items-center hidden gap-6 sm:flex">
          <ScrollLink
            to="features"
            spy="{true}"
            smooth="{true}"
            duration="{1000}"
            class="text-white transition cursor-pointer text-opacity-60 hover:text-opacity-100"
          >
            Features
          </ScrollLink>

          <ScrollLink
            to="product"
            spy="{true}"
            smooth="{true}"
            duration="{1000}"
            class="text-white transition cursor-pointer text-opacity-60 hover:text-opacity-100"
          >
            Product
          </ScrollLink>
          <ScrollLink
            to="faqs"
            spy="{true}"
            smooth="{true}"
            duration="{1000}"
            class="text-white transition cursor-pointer text-opacity-60 hover:text-opacity-100"
          >
            FAQs
          </ScrollLink>

          <RouterLink to="/dashboard">
            <button class="px-4 py-2 bg-white rounded-lg">Get Started</button>
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
        <h1 class="mt-6 font-bold text-center sm:text-9xl text-7xl">
          Prep Smart<br />Stand Apart
        </h1>
        <p class="mt-8 text-lg text-center">
          From conquering chapters to crushing quizzes, we’ve got you covered.
          <br />
          Perfect for students, procrastinators, and that one overachiever in
          your class.
        </p>
      </div>

      <div class="flex justify-center mt-8">
        <RouterLink to="/dashboard">
          <button class="px-4 py-2 font-medium text-black bg-white rounded-lg">
            Get Started
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
  <div className="text-white bg-black py-[20px] ">
    <div className="container trusted-by">
      <h2 className="text-xl text-center">Trusted By</h2>
      <div className="flex flex-wrap items-center justify-center gap-16 images">
        <img class="w-[150px]" :src="batman" alt="batman logo" />
        <img class="w-[80px]" :src="dc" alt="dc logo" />
        <img class="w-[150px]" :src="superman" alt="superman logo" />
      </div>
    </div>
  </div>
  <Features />
  <Product />
  <FAQs />
</template>






<style scoped>
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
  margin-top: 2.5px;
  font-size: 20px;
  opacity: 0;
  transition: all 0.3s ease;
}

a:hover ion-icon {
  opacity: 1;
  transform: translateX(10px);
}

.hamburger ion-icon {
  color: white;
  font-size: 2rem;
}

.rainbow-text {
  background-image: linear-gradient(
    to right,
    #f97aff,
    #2fd8fe,
    #fffc3e,
    #92ff6a,
    #2fd8fe,
    #f97aff
  );
  background-size: 300%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: consolas;
  font-weight: 600;
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
  letter-spacing: -9px;
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
  background: radial-gradient(closest-side, #000 80%, #ddff00);
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
