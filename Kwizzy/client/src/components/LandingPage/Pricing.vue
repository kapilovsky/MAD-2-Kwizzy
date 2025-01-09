<script setup>
import check from "../../assets/images/icons/check.svg";
const plans = [
  {
    name: "Basic",
    price: "$0",
    period: "/month",
    tagline: "For the curious minds",
    features: [
      "Access to all quizzes",
      "No ads, no distractions",
      "Full dashboard features",
      "Basic progress tracking",
    ],
  },
  {
    name: "Pro",
    price: "Priceless",
    period: "/forever",
    tagline: "For the overachievers",
    features: [
      "Extra laughs included",
      "Premium progress insights",
      "Still completely free",
      "Priority support (when I build it)",
    ],
    popular: true,
  },
  {
    name: "Business",
    price: "$0",
    period: "/lifetime",
    tagline: "For the ambitious",
    features: [
      "Everything in Premium",
      "Early access to new features",
      "Advanced analytics",
      "Did I mention it's free?",
    ],
  },
];
</script>

<template>
  <div
    id="pricing"
    class="text-white bg-black py-[72px] sm:py-24 bg-gradient-to-t from-[#21034d] to-black"
  >
    <div class="container">
      <!-- Header -->
      <h2 class="text-5xl font-bold tracking-tighter text-center sm:text-6xl">
        Free Forever. Because Why Not.
      </h2>
      <div class="max-w-xl mx-auto">
        <p class="mt-5 text-xl text-center text-white/70">
          Choose your flavor of free. Yes, they're all free. I just made
          multiple tiers to look professional.
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-16 mt-16 sm:px-24 px-10">
        <div
          v-for="(plan, index) in plans"
          :key="index"
          class="pricing-card relative group"
        >
          <!-- Card Content -->
          <div
            class="relative px-6 py-8 bg-black border border-white/10 rounded-xl z-10 card"
          >
            <!-- Popular Badge -->
            <div
              v-if="plan.popular"
              class="absolute -top-4 left-1/2 -translate-x-1/2 bg-[#000000] px-4 py-1 rounded-lg text-sm font-medium border border-[#380296]"
            >
              <span class="popular-badge">Most Popular</span>
            </div>

            <!-- Plan Details -->
            <div class="text-center mb-8">
              <h3 class="text-xl font-bold mb-2">{{ plan.name }}</h3>
              <div class="text-3xl font-bold mb-2 price">
                {{ plan.price }}
                <span class="text-lg font-normal text-white/70">{{
                  plan.period
                }}</span>
              </div>
              <p class="text-white/70">{{ plan.tagline }}</p>
            </div>

            <!-- Features -->
            <ul class="space-y-4 mb-8">
              <li
                v-for="(feature, featureIndex) in plan.features"
                :key="featureIndex"
                class="flex items-center text-white/80"
              >
                <!-- <ion-icon
                  name="checkmark-sharp"
                  class="mr-3 text-green-400"
                ></ion-icon> -->
                <component :is="check" class="mr-3 fill-[##4ade80]" />
                {{ feature }}
              </li>
            </ul>

            <!-- Button -->
            <button
              class="w-full py-3 px-6 bg-white text-black rounded-lg font-medium transition-all hover:bg-white/90"
            >
              Get Started
            </button>
          </div>

          <!-- Gradient Border Effect -->
          <div
            class="absolute inset-[-1.5px] rounded-xl bg-gradient-to-br from-[#d9ff00] to-[#5900ff0b] opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            style="z-index: 0"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#pricing {
  font-family: Inter;
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

.pricing-card {
  transition: transform 0.3s ease;
}

.pricing-card:hover {
  transform: translateY(-8px);
}

/* Mask for gradient border */
.pricing-card > div:first-child {
  background: black;
  transition: all 0.3s ease;
}

/* Optional: Add floating animation */
@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.pricing-card {
  animation: float 6s ease-in-out infinite;
}

.pricing-card:nth-child(2) {
  animation-delay: -2s;
}

.pricing-card:nth-child(3) {
  animation-delay: -4s;
}

.pricing-card li {
  transition: transform 0.2s ease;
}

.pricing-card li:hover {
  transform: translateX(8px);
}

.pricing-card .price {
  background: linear-gradient(to right, #fff, #a855f7);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.popular-badge {
  background-image: linear-gradient(
    to right,
    #f97aff,
    #a855f7,
    #f7f464,
    #aaf68e,
    #2fd8fe,
    #f97aff
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
  padding: 0px 8px;
}
</style>
