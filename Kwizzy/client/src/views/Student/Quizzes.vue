<template>
  <Loader v-if="isLoading" />
  <div v-else>
    <div class="absolute sm:top-6 top-16">
      <div class="sm:w-[450px] w-[300px]">
        <SearchBar @search="handleSearch" placeholder="Search chapters..." />
      </div>
    </div>

    <div class="sm:mt-4 mt-14">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-2 text-gray-600 text-sm mb-4">
        <RouterLink
          :to="{
            name: 'student-dashboard',
            params: {
              id: studentId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >Dashboard</RouterLink
        >
        <span>/</span>
        <RouterLink
          :to="{
            name: 'view-subjects',
            params: {
              id: studentId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >Subjects</RouterLink
        >
        <span>/</span>
        <RouterLink
          :to="{
            name: 'subject',
            params: {
              id: studentId,
              subjectId: subjectId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >{{ subject?.name }}</RouterLink
        >

        <span>/</span>
        <span class="text-black sohne-mono">{{ chapter?.name }}</span>
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
      </div>

      <div class="mb-4">
        <h2
          class="sm:text-5xl text-3xl font-semibold sohne tracking-tighter sm:tracking-[-2px]"
        >
          Quizzes
        </h2>
      </div>

      <!-- Chapter Quizzes -->
      <div>
        <div class="px-2">
          <table class="w-full">
            <thead>
              <tr class="text-left sm:text-sm text-xs border-b-2 border-black">
                <th>Quiz Name</th>
                <th>Questions</th>
                <th class="sm:table-cell hidden">Time Limit［HH:MM］</th>
                <th>Price</th>
                <th class="sm:table-cell hidden">Deadline</th>
                <th class="sm:table-cell hidden">Single Attempt Only</th>
                <th class="text-right px-2">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="quiz in filteredQuizzes"
                :key="quiz.id"
                class="border-b-2 text-xs sm:text-sm border-black hover:bg-[#fff9f0]"
              >
                <td class="py-2 relative">
                  <span class="absolute top-[2px] left-[-10px]">&lhblk;</span>
                  <RouterLink
                    :to="{
                      name: 'quiz',

                      params: {
                        id: route.params.id,
                        quizId: quiz.id,
                        subjectId: subjectId,
                        chapterId: chapterId,
                      },
                    }"
                  >
                    &nbsp;&nbsp;<span class="hover:text-[#0000ff]">{{
                      quiz.name
                    }}</span>
                  </RouterLink>
                </td>
                <td class="py-2">
                  {{ quiz.question_count }}
                </td>
                <td class="py-2 sm:table-cell hidden">
                  {{ quiz.time_duration }}
                </td>
                <td class="py-2">
                  {{ quiz?.price ? `₹${quiz.price}` : "Free" }}
                </td>
                <td class="py-2 sm:table-cell hidden">
                  <div class="flex items-center gap-2 font-mono">
                    <span
                      class="w-2 h-2 rounded-full"
                      :class="getDeadlineStatusClass(quiz)"
                    ></span>
                    {{ quiz?.deadline ? `${quiz.deadline} IST` : "None" }}
                  </div>
                </td>

                <td class="py-2 sm:table-cell hidden">
                  {{ quiz.one_attempt_only }}
                </td>

                <td class="p-2 text-right">
                  <RouterLink
                    class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400 text-right"
                    @click="handleNavigation"
                    :to="{
                      name: 'quiz',

                      params: {
                        id: route.params.id,
                        quizId: quiz.id,
                        subjectId: subjectId,
                        chapterId: chapterId,
                      },
                    }"
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
import { ref, onMounted, computed } from "vue";
import { RouterLink, useRoute } from "vue-router";
import SearchBar from "@/components/Admin/SearchBar.vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import Loader from "@/components/Loader.vue";
import { BreadcrumbsStore } from "@/stores/breadcrumbsStore";

const breadcrumbStore = BreadcrumbsStore();

const isLoading = ref(false);
const route = useRoute();
const subjectId = ref(route.params.subjectId);
const chapterId = ref(route.params.chapterId);
const subject = ref(null);
const chapter = ref(null);
const quizzes = ref([]);
const searchQuery = ref("");
const subjectName = ref(null);
const chapterName = ref(null);

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const student = ref(props.student);
const studentId = student.value.id;

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
      axios.get(`${API_URL}/quizzes/chapter/${chapterId.value}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);

    // Set data
    chapter.value = chapterRes.data;
    subject.value = subjectRes.data;
    chapterName.value = chapterRes.data.name;
    subjectName.value = subjectRes.data.name;
    quizzes.value = quizzesRes.data.quizzes;
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

const handleNavigation = () => {
  breadcrumbStore.setBreadcrumbs({
    subjectName: subjectName.value,
    chapterName: chapterName.value,
    subjectId: subjectId.value,
    chapterId: chapterId.value,
  });
  console.log(chapterName.value, subjectName.value, "before navigation ");
};

const formatDateForInput = (dateString) => {
  if (!dateString) return "";

  // Parse the date string (DD-MM-YYYY HH:mm)
  const [datePart, timePart] = dateString.split(" ");
  const [day, month, year] = datePart.split("-");

  // Create the formatted string (YYYY-MM-DDThh:mm)
  return `${year}-${month}-${day}T${timePart}`;
};

const getDeadlineStatusClass = (quiz) => {
  if (!quiz.deadline) return "bg-green-400";

  const deadline = formatDateForInput(quiz.deadline);
  const now = new Date();

  return new Date(deadline) < now
    ? "bg-red-500" // Expired
    : "bg-green-500"; // Active
};

onMounted(async () => {
  await fetchData();
});
</script>

<style scoped>
/* Add these classes if not already present in your global styles */
.bg-red-500 {
  background-color: #ef4444;
}

.bg-green-500 {
  background-color: #10b981;
}

.bg-gray-400 {
  background-color: #9ca3af;
}
</style>
