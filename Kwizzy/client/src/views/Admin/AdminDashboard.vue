<script setup>
import Sidebar from "@/components/Admin/Sidebar.vue";
import SubjectCard from "@/components/Admin/SubjectCard.vue";
import { ref, onMounted, computed } from "vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import CreateSubject from "@/components/Admin/AddSubject.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";
import logo from "../../assets/images/landing-page/white logo.png";

const allSubjects = ref([]); // Store all subjects
const searchQuery = ref(""); // Store search query
const isCreateModalOpen = ref(false);

// Computed property for filtered subjects
const filteredSubjects = computed(() => {
  if (!searchQuery.value) return allSubjects.value;

  return allSubjects.value.filter(
    (subject) =>
      subject.name.toLowerCase().includes(searchQuery.value) ||
      subject.description.toLowerCase().includes(searchQuery.value)
  );
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

const handleCreateSubject = (newSubject) => {
  fetchSubjects();
  isCreateModalOpen.value = false;
};

const fetchSubjects = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }

    const response = await axios.get(`${API_URL}/subject`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    allSubjects.value = response.data.subjects.map((subject) => ({
      ...subject,
      image: `${API_URL}/uploads/subjects/${subject.subject_image}`,
    }));
    console.log("Fetched subjects:", subjects.value, subjects.value[0].image);
  } catch (error) {
    console.error(
      "Error fetching subjects:",
      error.response?.data || error.message
    );
  }
};

onMounted(() => {
  fetchSubjects();
});
</script>

<template>
  <Sidebar>
    <header class="h-16 bg-white flex items-center justify-between gap-6">
      <div class="flex items-center flex-1">
        <div class="flex-1 max-w-lg">
          <div class="relative">
            <SearchBar
              @search="handleSearch"
              placeholder="Search subjects..."
            />
          </div>
        </div>
      </div>

      <!-- Right Side Icons -->
      <div class="flex items-center">
        <div class="flex items-center gap-4">
          <img
            :src="logo"
            alt="User avatar"
            class="w-8 h-8 rounded-full mix-blend-difference"
          />
          <span class="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </header>
    <div class="mb-6">
      <h1 class="text-4xl font-bold">Subjects</h1>
      <p>Manage and organize the subjects</p>
    </div>
    <SubjectCard :subjects="filteredSubjects" />
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
