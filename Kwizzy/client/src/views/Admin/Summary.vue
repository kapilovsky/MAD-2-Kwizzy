<template>
  <Loader v-if="isLoading" />

  <Sidebar v-else>
    <div class="p-6">
      <h2
        @mouseover="addCursorState('heading-hover')"
        @mouseout="removeCursorState('heading-hover')"
        class="sm:text-5xl text-3xl mb-6 sohne-mono font-bold w-fit"
      >
        Summary📒
      </h2>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div
          @mouseover="addCursorState('hovering')"
          @mouseout="removeCursorState('hovering')"
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 sohne uppercase"
          >
            Total Students
          </h3>
          <p class="text-3xl font-bold">{{ total_students }}</p>
        </div>
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
          @mouseover="addCursorState('hovering')"
          @mouseout="removeCursorState('hovering')"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Total Subjects
          </h3>
          <p class="text-3xl font-bold">{{ total_subjects }}</p>
        </div>
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
          @mouseover="addCursorState('hovering')"
          @mouseout="removeCursorState('hovering')"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Total Chapters
          </h3>
          <p class="text-3xl font-bold">{{ total_chapters }}</p>
        </div>
        <div
          class="bg-white hover:bg-[#b20811] hover:text-white transition-all duration-200 group rounded-xl p-5"
          @mouseover="addCursorState('hovering')"
          @mouseout="removeCursorState('hovering')"
        >
          <h3
            class="text-sm text-gray-500 group-hover:text-white transition-all duration-200 uppercase"
          >
            Total Quizzes
          </h3>
          <p class="text-3xl font-bold">{{ total_quizzes }}</p>
        </div>
        <!-- Add more stat cards -->
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SubjectPerformance :data="subject_performance" />
        <QualificationChart :data="qualification_distribution" />
        <PerformanceDistribution :data="performance_distribution" />
        <ActivityChart :data="activity" />
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import { useCursor } from "@/composables/useCursor";
import Sidebar from "@/components/Admin/Sidebar.vue";
import ActivityChart from "@/components/Admin/charts/ActivityChart.vue";
import QualificationChart from "@/components/Admin/charts/QualificationChart.vue";
import SubjectPerformance from "@/components/Admin/charts/SubjectPerformance.vue";
import PerformanceDistribution from "@/components/Admin/charts/PerformanceDistribution.vue";

const activity = ref(null);
const statistics = ref(null);
const total_quizzes = ref(null);
const total_students = ref(null);
const total_subjects = ref(null);
const total_chapters = ref(null);
const subject_performance = ref(null);
const performance_distribution = ref(null);
const qualification_distribution = ref(null);
const API_URL = import.meta.env.VITE_API_URL;
const isLoading = ref(true);

const { addCursorState, removeCursorState } = useCursor();
const fetchStatistics = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("Token not found");
    }
    const response = await axios.get(`${API_URL}/charts`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    statistics.value = response.data;
    performance_distribution.value = response.data.performance;
    activity.value = response.data.activity;
    qualification_distribution.value = response.data.qualifications;
    subject_performance.value = response.data.subjects;
    total_subjects.value = response.data.subjects.totalSubjects;
    total_chapters.value = response.data.subjects.totalChapters;
    total_quizzes.value = response.data.subjects.totalQuizzes;
    console.log("stats", statistics.value);
    total_students.value = activity.value.data.reduce(
      (acc, curr) => acc + curr,
      0
    );
  } catch (error) {
    console.error("Error fetching statistics:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStatistics();
});
</script>
