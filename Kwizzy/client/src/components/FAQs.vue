<script setup>
import { ref } from "vue";

// FAQ items
const items = [
  {
    question: "Is it really free?",
    answer: "Yes! Unless you count your time and effort.",
  },
  {
    question: "Can I cheat?",
    answer:
      "Well, Kwizzy doesn’t judge… but remember, cheaters never prosper. Plus, the only person you’re fooling is your own ego. We recommend winning with your brains, not your browser tabs! 😉",
  },
  {
    question: "What if I forget my password?",
    answer:
      "First, try 'password123' because let's be honest, that was probably it. If that fails, we have a fancy 'Forgot Password' button that's been waiting for its moment to shine.",
  },
  {
    question: "What if I fail all the quizzes?",
    answer:
      "Then you’ll join our exclusive “Kwizzy’s Humble Learners Club.” It’s not a real club, but hey, failure is the first step to becoming a quiz master!",
  },
  {
    question: "Is this app addictive?",
    answer:
      " Let’s just say you might “accidentally” miss your bedtime. But hey, learning is productive, right?",
  },
  {
    question: "Can Kwizzy help me impress my crush?",
    answer:
      "Absolutely! Just casually mention your latest quiz score and watch the sparks fly. Or not. We can’t guarantee anything.",
  },
];

// Track which item is open
const openItemIndex = ref(null);

const toggleItem = (index) => {
  openItemIndex.value = openItemIndex.value === index ? null : index;
};
</script>

<template>
  <div
    id="faqs"
    class="text-white bg-black py-[72px] sm:py-24 bg-gradient-to-b from-[#21034d] to-black"
  >
    <div class="container">
      <h2 class="text-5xl font-bold tracking-tighter text-center sm:text-6xl">
        Frequently asked questions
      </h2>
      <div class="max-w-xl mx-auto">
        <p class="mt-5 text-xl text-center text-white/70">
          Questions About the Quiz App? How Ironic.
        </p>
      </div>
      <div class="max-w-2xl mx-auto mt-12">
        <div
          v-for="(item, index) in items"
          :key="index"
          class="border-b py-7 border-white/30 cursor-pointer"
          @click="toggleItem(index)"
        >
          <div class="flex items-center justify-between mt-10">
            <h3 class="text-lg font-bold">{{ item.question }}</h3>
            <ion-icon
              :name="openItemIndex === index ? 'remove-sharp' : 'add-sharp'"
            ></ion-icon>
          </div>
          <transition
            name="accordion"
            enter-active-class="transition-all duration-300"
            leave-active-class="transition-all duration-300"
          >
            <div
              v-show="openItemIndex === index"
              class="mt-4 text-white/70 overflow-hidden"
            >
              {{ item.answer }}
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.accordion-enter-from,
.accordion-leave-to {
  height: 0;
  opacity: 0;
  margin-top: 0;
}

.accordion-enter-to,
.accordion-leave-from {
  height: auto;
  opacity: 1;
  margin-top: 16px;
}
</style>
