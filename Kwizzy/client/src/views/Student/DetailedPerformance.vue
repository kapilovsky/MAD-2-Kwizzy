<template>
  <Loader v-if="isLoading" />

  <div v-else>
    <div class="absolute sm:top-6 top-16">
      <div class="sm:w-[450px] w-[300px]">
        <SearchBar @search="handleSearch" placeholder="Search Quiz Names..." />
      </div>
    </div>

    <div
      class="rounded-3xl sm:px-8 px-4 py-6 mt-8 shadow-sm transition-all hover:shadow-lg bg-[#fff9f0]"
    >
      <div class="flex items-center justify-between mb-6">
        <h3
          class="font-bold sm:text-[48px] text-3xl text-orange-600 tracking-tighter"
        >
          Quiz History
        </h3>
      </div>
      <table class="w-full border-collapse">
        <thead>
          <tr
            class="text-left text-orange-600 sm:text-sm text-xs border-b-2 border-black"
          >
            <th class="p-2">Quiz Title</th>
            <th class="p-2">Score</th>
            <th class="p-2 sm:block hidden">Accuracy</th>
            <th class="p-2">Completion Date</th>
            <th class="text-right p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="text-xs sm:text-sm"
            v-for="quiz in filteredQuizzes"
            :key="quiz.id"
          >
            <td class="p-2">{{ quiz.quiz_name }}</td>
            <td class="p-2">{{ quiz.marks_scored }}</td>
            <td class="p-2 sm:block hidden">{{ quiz.percentage }}%</td>
            <td class="p-2">{{ formatDate(quiz.completed_at) }}</td>
            <td class="text-right">
              <RouterLink
                :to="{
                  name: 'quiz-results',
                  params: {
                    id: props.student.student_info.id,
                    quizId: quiz.quiz_id,
                  },
                  query: {
                    resultId: quiz.quiz_result_id,
                  },
                }"
                class="text-orange-500 hover:font-bold sm:text-sm text-xs sohne-mono bg-orange-200 sm:px-5 sm:py-1 py-[4px] rounded-md"
              >
                View Details
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { studentService } from "@/services/studentService";
import SearchBar from "@/components/Admin/SearchBar.vue";
import Loader from "@/components/Loader.vue";

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const student = ref();
const allQuizzes = ref([]);
const searchQuery = ref("");
const isLoading = ref(false);

const getAllquizzes = async () => {
  try {
    isLoading.value = true;
    const response = await studentService.getStudent(
      props.student.student_info.id
    );
    student.value = response;
    allQuizzes.value = response.detailed_performance;
    console.log("student", student.value);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

const filteredQuizzes = computed(() => {
  if (!searchQuery.value) {
    return allQuizzes.value;
  }
  return allQuizzes.value.filter((quiz) =>
    quiz.quiz_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(() => {
  getAllquizzes();
});
</script>
