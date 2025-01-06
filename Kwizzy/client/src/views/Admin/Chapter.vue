<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import CloseIcon from "../../assets/images/icons/close.svg";
import AddIcon from "../../assets/images/icons/add.svg";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";
import logo from "../../assets/images/landing-page/white logo.png";
import { useToast } from "@/composables/useToast";
const isLoading = ref(false);

const route = useRoute();
const router = useRouter();
const toast = useToast();
const subjectId = ref(route.params.subjectId);
const chapterId = ref(route.params.chapterId);
const subject = ref(null);
const chapter = ref(null);
const quizzes = ref([]);
const searchQuery = ref("");

const fetchData = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }

    // Fetch data
    const [chapterRes, subjectRes, quizzesRes] = await Promise.all([
      axios.get(`${API_URL}/chapter/${chapterId.value}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get(`${API_URL}/subject/${subjectId.value}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get(`${API_URL}/quizzes`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);

    // Set data
    chapter.value = chapterRes.data;
    subject.value = subjectRes.data;
    quizzes.value = quizzesRes.data.quizzes;
    console.log("Quizzes:", quizzes.value);
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};

const deleteQuiz = async (quizId) => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");
    const response = await axios.delete(`${API_URL}/quizzes/${quizId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    toast.success(response.data.message);
    await fetchData();
  } catch (error) {
    toast.error(error.response?.data?.message || "Error deleting quiz");
    console.error("Error deleting quiz:", error);
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
  await fetchData();
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

    <div class="flex justify-between items-center mb-4">
      <h2 class="text-5xl font-semibold sohne tracking-[-2px]">Quizzes</h2>
      <RouterLink
        :to="`/admin/subject/${subjectId}/chapter/${chapterId}/quiz/create`"
        class="px-4 py-2 bg-black text-white rounded-lg hover:bg-[#161616] hover:scale-95 transition-all duration-200 flex items-center gap-2 font-semibold"
      >
        <component :is="AddIcon" class="w-5 h-5" />
        Create Quiz
      </RouterLink>
    </div>

    <!-- Chapter Quizzes -->
    <div>
      <div class="px-2">
        <table class="w-full">
          <thead>
            <tr class="text-left text-sm border-b-2 border-black">
              <th>Quiz Name</th>
              <th>Questions</th>
              <th>Time Limit［HH:MM］</th>
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
                <span class="absolute top-[2px] left-[-10px]">&lhblk;</span>
                <RouterLink
                  :to="`/admin/subject/${subjectId}/chapter/${chapterId}/quiz/${quiz.id}`"
                >
                  &nbsp;&nbsp;<span class="hover:text-[#0000ff]">{{
                    quiz.name
                  }}</span>
                </RouterLink>
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
                  <RouterLink
                    :to="`/admin/subject/${subjectId}/chapter/${chapterId}/quiz/${quiz.id}/edit`"
                  >
                    <button
                      class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400"
                    >
                      EDIT
                    </button>
                  </RouterLink>

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
