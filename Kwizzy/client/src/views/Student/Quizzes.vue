<template>
  <Loader v-if="isLoading" />
  <div v-else>
    <div class="absolute top-6">
      <div class="w-[450px]">
        <SearchBar @search="handleSearch" placeholder="Search chapters..." />
      </div>
    </div>

    <div class="my-8">
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
          <span class="font-medium sohne-mono">{{
            chapter?.students || 0
          }}</span>
        </div>
      </div>

      <div class="mb-4">
        <h2 class="text-5xl font-semibold sohne tracking-[-2px]">Quizzes</h2>
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
                <th class="text-right px-2">Action</th>
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

                <td class="p-2 text-right">
                  <RouterLink
                    class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400 text-right"
                    :to="`${route.path}/quiz/${quiz.id}`"
                  >
                    VIEW
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import SearchBar from "@/components/Admin/SearchBar.vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import Loader from "@/components/Loader.vue";

const isLoading = ref(false);
const route = useRoute();
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
