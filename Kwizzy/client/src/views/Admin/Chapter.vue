<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import CloseIcon from "../../assets/images/icons/close.svg";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";
import logo from "../../assets/images/landing-page/white logo.png";
const isLoading = ref(false);

const route = useRoute();
const router = useRouter();
const subjectId = ref(route.params.subjectId);
const chapterId = ref(route.params.chapterId);
const subject = ref(null);
const chapter = ref(null);
const quizzes = ref([]);
const searchQuery = ref("");

const fetchChapter = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }
    const response = await axios.get(`${API_URL}/chapter/${chapterId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    chapter.value = response.data;
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching chapter:", error);
    isLoading.value = false;
  } finally {
    isLoading.value = false;
  }
};

const fetchSubject = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }
    const response = await axios.get(`${API_URL}/subject/${subjectId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    subject.value = response.data;
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching subject:", error);
    isLoading.value = false;
  } finally {
    isLoading.value = false;
  }
};

const fetchQuizzes = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }
    const response = await axios.get(`${API_URL}/quizzes`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: { chapter_id: chapterId.value },
    });
    quizzes.value = response.data.quizzes;
    console.log("Fetched quizzes:", quizzes.value);
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching quizzes:", error);
    isLoading.value = false;
  } finally {
    isLoading.value = false;
  }
};

const filteredQuizzes = computed(() => {
  if (!searchQuery.value) {
    return quizzes.value;
  }

  return quizzes.value.filter((quiz) =>
    quiz.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

onMounted(async () => {
  await fetchChapter();
  await fetchSubject();
  await fetchQuizzes();
});
</script>

<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <header class="h-16 bg-white flex items-center justify-between gap-6 mb-2">
      <!-- SEARCHBAR -->
      <div class="flex items-center flex-1">
        <div class="flex-1 max-w-lg">
          <div class="relative">
            <SearchBar @search="handleSearch" placeholder="Search quizzes..." />
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

    <!-- Breadcrumbs -->
    <div class="flex items-center gap-2 text-sm mb-6">
      <RouterLink to="/admin" class="text-gray-500 hover:text-black sohne-mono">
        Subjects
      </RouterLink>
      <span class="text-gray-500">/</span>
      <RouterLink
        :to="`/admin/subject/${subject?.id}`"
        class="text-gray-500 hover:text-black sohne-mono"
      >
        {{ subject?.name }}
      </RouterLink>
      <span class="text-gray-500">/</span>
      <span class="font-medium sohne-mono">{{ chapter?.name }}</span>
    </div>

    <!-- Chapter Details -->
    <div class="flex items-center gap-2 text-sm mb-2">
      <span class="font-bold sohne-mono text-3xl">{{ chapter?.name }}</span>
    </div>

    <div class="flex items-center gap-2 text-sm mb-6">
      <span class="font-medium sohne-mono">{{ chapter?.description }}</span>
    </div>
    <div class="flex items-center gap-12 text-sm mb-10">
      <div class="flex items-center gap-2 text-sm">
        <span class="text-gray-500 sohne-mono">Quizzes:</span>
        <span class="font-medium sohne-mono">{{
          chapter?.total_quizzes || 0
        }}</span>
      </div>

      <div class="flex items-center gap-2 text-sm">
        <span class="text-gray-500 sohne-mono">Students:</span>
        <span class="font-medium sohne-mono">{{ chapter?.students || 0 }}</span>
      </div>
    </div>

    <!-- Chapter Quizzes -->
    <div>
      <div>
        <h2 class="text-5xl font-semibold sohne tracking-[-2px] mb-4">
          Quizzes
        </h2>
      </div>
      <div class="px-2">
        <table class="w-full">
          <thead>
            <tr class="text-left text-sm border-b-2 border-black">
              <th>Quiz Name</th>
              <th>Questions</th>
              <th>Time Limit</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="quiz in filteredQuizzes"
              :key="quiz.id"
              class="border-b-2 border-black"
            >
              <td class="py-2 relative">
                <span class="absolute top-[2px]">&lhblk;</span>
                &nbsp;&nbsp;<span class="font-medium">{{ quiz.name }}</span>
              </td>
              <td class="py-2">
                <span class="font-medium">{{ quiz.question_count }}</span>
              </td>
              <td class="py-2">
                <span class="font-medium">{{ quiz.time_duration }}</span>
              </td>
              <td class="py-2">
                <span class="font-medium">{{ quiz.price || "Free" }}</span>
              </td>

              <td class="py-2">
                <div class="flex items-center gap-2">
                  <button
                    class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400"
                  >
                    EDIT
                  </button>

                  <button
                    @click="deleteQuiz(quiz.id)"
                    class="py-[2px] px-1 text-gray-600 hover:text-[#ff0a0a] sohne-mono text-[12px] border-dotted border border-gray-400"
                  >
                    DELETE
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Sidebar>
</template>

<style></style>
