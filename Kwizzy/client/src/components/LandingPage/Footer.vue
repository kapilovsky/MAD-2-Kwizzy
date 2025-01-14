<script setup>
const currentYear = new Date().getFullYear();
import logo from "../../assets/images/landing-page/white logo.png";

const footerLinks = {
  product: {
    title: "Product",
    links: [
      { name: "Home", id: "#" },
      { name: "Features", id: "#features" },
      { name: "Product Showcase", id: "#product" },
      { name: "Pricing", id: "#pricing" },
      { name: "Testimonials", id: "#testimonials" },
      { name: "FAQs", id: "#faqs" },
    ],
  },
  social: {
    title: "Social",
    links: [
      { name: "Twitter", id: "https://x.com/k4p1ll", icon: "logo-twitter" },
      { name: "GitHub", id: "https://github.com/k4p1l", icon: "logo-github" },
      {
        name: "LinkedIn",
        id: "https://www.linkedin.com/in/k4p1l/",
        icon: "logo-linkedin",
      },
      {
        name: "Instagram",
        id: "https://www.instagram.com/k4p1ll/",
        icon: "logo-instagram",
      },
    ],
  },
};
</script>

<template>
  <footer class="relative bg-black text-white overflow-hidden">
    <div class="container">
      <div
        class="absolute top-0 left-0 w-full h-full bg-gradient-to-t from-[#1f134f] to-black"
      ></div>

      <!-- Main Footer Content -->
      <div class="relative container pb-10 px-16">
        <!-- Links Section -->
        <div
          class="flex sm:flex-row flex-col justify-between items-center gap-8 py-2 pb-10"
        >
          <div>
            <img
              class="w-[200px] sm:w-[300px] mix-blend-exclusion"
              :src="logo"
              alt=""
            />
          </div>

          <div class="flex justify-between sm:w-[30%]">
            <div
              v-for="(section, key) in footerLinks"
              :key="key"
              class="space-y-6 px-2"
            >
              <h4 class="font-bold text-lg">{{ section.title }}</h4>
              <ul class="space-y-4">
                <li v-for="link in section.links" :key="link.name">
                  <a
                    :href="link.id"
                    target="_blank"
                    class="text-white/70 hover:text-white flex items-center gap-2 transition-colors group"
                  >
                    <ion-icon
                      v-if="link.icon"
                      :name="link.icon"
                      class="text-xl group-hover:scale-110 transition-transform"
                    ></ion-icon>
                    {{ link.name }}
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Bottom Section -->
        <div
          class="pt-8 flex flex-col md:flex-row justify-start items-center gap-4"
        >
          <div class="gradient-text">Kwizzy</div>
          <div class="flex items-center gap-2 sm:mb-14 mb-32">
            <span class="text-white"
              >© {{ currentYear }}. All rights reserved. I mean, the right to
              brag about this project.</span
            >
          </div>
        </div>

        <!-- Easter Egg -->
        <div
          class="absolute bottom-16 sm:bottom-4 text-white/50 text-sm text-center hover:text-[#ddff00] transition-colors cursor-help easter"
        >
          Made with chai-tea and questionable life choices. <br />
          *No textbooks were harmed in the making of this platform.
        </div>
      </div>

      <!-- Decorative Elements -->

      <div
        class="absolute bottom-0 right-0 w-96 h-96 bg-fuchsia-600/10 rounded-full filter blur-3xl pointer-events-none"
      ></div>
      <div
        class="absolute top-1/2 left-0 w-96 h-96 bg-pink-700/20 rounded-full filter blur-3xl pointer-events-none"
      ></div>
    </div>
  </footer>
</template>

<style scoped>
.container {
  max-width: 1800px;
  margin: 0 auto;
}

img {
  user-select: none;
  pointer-events: none;
}
.gradient-text {
  background: linear-gradient(70deg, #caafff, #1c0e38);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: Miracle;
  font-size: 280px;
  position: absolute;
  right: -20px;
  bottom: -140px;
  user-select: none;
  pointer-events: none;
}

@media (max-width: 768px) {
  .gradient-text {
    font-size: 145px;
    left: 0px;
    bottom: -150px;
  }

  footer {
    padding-bottom: 120px;
  }

  .easter {
    right: 2px;
  }
}

/* Hover Effects */
a {
  position: relative;
  width: fit-content;
  cursor: none;
}

a::after {
  content: "";
  position: absolute;
  width: 0;
  height: 2.2px;
  bottom: -2.2px;
  left: 0;
  background: linear-gradient(to right, #e879f9, #6366f1);
  transition: width 0.3s ease;
}

a:hover::after {
  width: 100%;
}

/* Input Focus Effect */
input:focus {
  box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
}

/* Optional: Add floating animation to decorative elements */
@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.footer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(168, 85, 247, 0.2),
    transparent
  );
}

button:hover {
  animation: none;
}

.easter {
  font-family: Browess Sovar;
  font-size: 18px;
  transition: all 0.3s ease;
}

.easter:hover {
  color: #ffffff;
  animation: flicker 0.1s infinite;
}

@keyframes flicker {
  0% {
    opacity: 1;
  }
  20% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.9;
  }
  80% {
    opacity: 0.2;
  }
  100% {
    opacity: 1;
  }
}
</style>
