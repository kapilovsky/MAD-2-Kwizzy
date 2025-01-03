<script setup>
import Sidebar from "@/components/Admin/Sidebar.vue";
import SubjectCard from "@/components/Admin/SubjectCard.vue";
import { ref } from "vue";
import CreateSubject from "@/components/Admin/CreateSubject.vue";
const isCreateModalOpen = ref(false);

const handleCreateSubject = (newSubject) => {
  // Handle subject creation logic
  console.log("New subject:", newSubject);
  isCreateModalOpen.value = false;
};
const subjects = ref([
  {
    id: 1,
    name: "Mathematics",
    description: "Advanced mathematical concepts and problem-solving",
    image: "src/assets/images/landing-page/app.jpg",
    studentCount: 150,
    quizCount: 12,
  },
  {
    id: 2,
    name: "Physics",
    description: "Study of matter, energy, and their interactions",
    image: "src/assets/images/landing-page/bg.png",
    studentCount: 120,
    quizCount: 8,
  },
  // Add more subjects...
]);
</script>

<template>
  <Sidebar>
    <div class="mb-6">
      <h1 class="text-4xl font-bold">Subjects</h1>
      <p>Manage and organize the subjects</p>
    </div>
    <SubjectCard :subjects="subjects" />
    <CreateSubject
      :is-open="isCreateModalOpen"
      @close="isCreateModalOpen = false"
      @create="handleCreateSubject"
    />
    <!-- Floating Add Subject Button -->
    <button
      @click="isCreateModalOpen = true"
      class="fixed bottom-6 sm:right-6 right-[calc(50%-80px)] z-30 flex items-center gap-2 px-4 py-3 bg-white hover:bg-black text-black hover:text-white font-semibold border-2 border-black rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
    >
      <svg
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 4v16m8-8H4"
        />
      </svg>
      <span>Add Subject</span>
    </button>
  </Sidebar>
</template>
