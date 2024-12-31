<script setup>
import bg from "../assets/images/landing-page/bg.png";
const Testimonials = [
  {
    name: "Kapil ",
    description: "Probably a real person",
    review:
      "I aced my exams because of Quiz Master! Or at least, I didn't fail spectacularly. Thanks, I guess?",
  },
  {
    name: "Alisha",
    description: "A Genz User",
    review:
      "Finally, a quiz app that doesn't look like it was made in the early 2000s.",
  },
  {
    name: "Sarah ",
    description: "A Biology Student",
    review:
      "I used to think mitochondria was a nightclub. Thanks to Kwizzy, I now know it's the powerhouse of the cell!",
  },
  {
    name: "Milo ",
    description: "Master of Excuses",
    review: "My dog ate my homework, but he couldn't eat my Kwizzy progress.",
  },
];
</script>

<template>
  <div id="testimonials">
    <div
      class="text-white bg-black bg-gradient-to-t from-black to-[#21034d] py-[72px] sm:py-24"
    >
      <div class="container">
        <h2
          class="text-6xl tracking-tighter font-bold text-center"
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1 }"
          :delay="300"
        >
          What They <br />
          <span>(Definitely Didn’t)</span> Say About Us
        </h2>
        <div class="max-w-xl mx-auto">
          <p
            class="mt-5 text-center text-white/70"
            v-motion
            :initial="{ opacity: 0, y: 50 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="500"
          >
            *Disclaimer: These reviews are 100% made up but still 100% accurate.
          </p>
        </div>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-16 px-4"
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0 }"
          :delay="500"
        >
          <div
            v-for="(item, index) in Testimonials"
            :key="index"
            class="testimonial-card relative group"
          >
            <div class="relative overflow-hidden rounded-xl h-[300px]">
              <!-- Background Image -->
              <img
                :src="bg"
                alt="background"
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />

              <!-- Content Overlay -->
              <div
                class="absolute inset-0 bg-gradient-to-t from-black/90 to-black/40 p-6 flex flex-col justify-end"
              >
                <p
                  class="text-lg font-medium mb-4 text-white/70 leading-snug review"
                >
                  "{{ item.review }}"
                </p>
                <p class="text-lg reviewer">
                  {{ item.name }}
                </p>
                <p class="text-sm text-white/60 reviewer-desc">
                  {{ item.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
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
.container h2 span {
  font-family: "Instrument Serif";
  font-weight: normal;
  font-style: italic;
}

.review {
  font-family: Inter;
}

.reviewer {
  font-family: "Instrument Serif";
  font-style: italic;
}

.reviewer-desc {
  font-family: Inter;
}

.testimonial-card {
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-8px);
}

/* Optional: Add a subtle glow effect on hover */
.testimonial-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 0.75rem;
  padding: 2px;
  background: linear-gradient(
    to bottom right,
    rgb(221, 255, 0.7),
    rgb(250, 174, 255, 0.5),
    rgba(255, 255, 255, 0.05)
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.testimonial-card:hover::after {
  opacity: 1;
}
</style>
