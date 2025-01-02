<!-- components/ExpandableCard.vue -->
<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const props = defineProps({
  subjects: {
    type: Array,
    required: true,
  },
});

const activeSubject = ref(null);
const isModalOpen = ref(false);
const modalRef = ref(null);

const handleKeyDown = (event) => {
  if (event.key === "Escape") {
    closeModal();
  }
};

const handleClickOutside = (event) => {
  if (modalRef.value && !modalRef.value.contains(event.target)) {
    closeModal();
  }
};

const closeModal = () => {
  activeSubject.value = null;
  isModalOpen.value = false;
  document.body.style.overflow = "auto";
};

const openModal = (subject) => {
  activeSubject.value = subject;
  isModalOpen.value = true;
  document.body.style.overflow = "hidden";
};

onMounted(() => {
  window.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
  document.body.style.overflow = "auto";
});
</script>

<template>
  <div class="relative">
    <!-- Modal Backdrop -->
    <Transition name="fade">
      <div
        v-if="isModalOpen"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
        @click="closeModal"
      ></div>
    </Transition>

    <!-- Modal -->
    <Transition name="slide-up">
      <div
        v-if="isModalOpen && activeSubject"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <div
          ref="modalRef"
          class="bg-white rounded-2xl w-full max-w-[500px] overflow-hidden shadow-xl"
        >
          <!-- Close Button -->
          <button
            @click="closeModal"
            class="absolute top-4 right-4 py-1 px-4 bg-[#ffffffdd] hover:bg-white transition-colors duration-200 flex items-center justify-center gap-2 backdrop-blur-sm font-mono"
          >
            [ESC]
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="3"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <!-- Subject Image -->
          <img
            :src="activeSubject.image"
            :alt="activeSubject.name"
            class="w-full h-60 object-cover"
          />

          <!-- Content -->
          <div class="p-6">
            <h3 class="text-xl font-semibold text-gray-900">
              {{ activeSubject.name }}
            </h3>
            <p class="mt-2 text-gray-700">
              {{ activeSubject.description }}
            </p>

            <!-- Stats -->
            <div class="mt-6 grid grid-cols-2 gap-4">
              <div class="text-center p-3 border-2 border-black rounded-lg">
                <p class="text-sm text-gray-900">Students</p>
                <p class="text-lg font-semibold text-gray-900">
                  {{ activeSubject.studentCount }}
                </p>
              </div>
              <div class="text-center p-3 border-2 border-black rounded-lg">
                <p class="text-sm text-gray-900">Quizzes</p>
                <p class="text-lg font-semibold text-gray-900">
                  {{ activeSubject.quizCount }}
                </p>
              </div>
            </div>

            <!-- Actions -->
            <div class="mt-6 flex space-x-3">
              <button
                class="flex-1 px-4 py-3 bg-black text-white rounded-full hover:bg-transparent border-2 border-black hover:text-black duration-300 font-semibold hover:-translate-y-1 transition-all shadow-lg hover:shadow-xl"
              >
                Edit Subject
              </button>
              <button
                class="flex-1 px-4 py-3 bg-transparent text-black rounded-full hover:bg-black hover:text-white duration-300 border-2 border-black font-semibold hover:-translate-y-1 transition-all shadow-lg hover:shadow-xl"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Subject Grid -->
    <div
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <div
        v-for="subject in subjects"
        :key="subject.id"
        @click="openModal(subject)"
        class="group cursor-pointer bg-[#fafafa] rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border-2 border-[#e5e7ebd6]"
      >
        <div class="relative">
          <img
            :src="subject.image"
            :alt="subject.name"
            class="w-full h-52 object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 group-hover:scale-105 transition-all duration-300"
          ></div>
        </div>

        <div class="p-3">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ subject.name }}
          </h3>
          <p class="mt-1 text-sm text-gray-600">
            {{ subject.description }}
          </p>

          <div class="mt-4 flex justify-between text-sm">
            <span class="text-gray-600">
              {{ subject.studentCount }} Students
            </span>
            <span class="text-gray-600"> {{ subject.quizCount }} Quizzes </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}

.slide-up-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-40px);
}

@media (max-width: 640px) {
  .fixed.bottom-6.right-6 {
    bottom: 1rem;
    right: 1rem;
  }
}
</style>
