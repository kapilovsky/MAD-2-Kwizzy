<!-- views/Admin/StudentDetails.vue -->
<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import logo from "@/assets/images/landing-page/white logo.png";
import { studentService } from "@/services/studentService";

const route = useRoute();
const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL;

const student = ref(null);
const loading = ref(true);
const recentQuizzes = ref([]);

const getRecentActivity = async () => {
  try {
    loading.value = true;
    recentQuizzes.value = await studentService.getRecentActivity(
      route.params.id
    );
  } catch (error) {
    console.error("Error:", error);
  } finally {
    loading.value = false;
  }
};

const fetchStudentDetails = async () => {
  try {
    loading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/student/${route.params.id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    student.value = response.data.student_info;
  } catch (error) {
    console.error("Error fetching student details:", error);
  } finally {
    loading.value = false;
  }
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
  fetchStudentDetails();
  getRecentActivity();
});
</script>

<template>
  <Sidebar>
    <!-- Header Section -->
    <div class="h-16 bg-white flex items-center justify-between mb-2">
      <button
        @click="router.back()"
        class="flex items-center gap-2 hover:bg-gray-100 px-3 py-1 rounded-lg transition-colors duration-200"
      >
        🡰
        <span class="sohne-mono">Back</span>
      </button>

      <div class="flex items-center gap-4">
        <img
          :src="logo"
          alt="User avatar"
          class="w-8 h-8 rounded-full mix-blend-exclusion"
        />
        <span class="text-sm font-medium text-gray-700">Admin</span>
      </div>
    </div>

    <!-- Main Content -->
    <div class="px-3">
      <Loader v-if="loading" />

      <template v-else>
        <!-- Student Header -->
        <div class="flex items-start justify-between mb-8">
          <div>
            <h1 class="text-4xl font-bold sohne-mono mb-2">Student Details</h1>
            <p class="text-neutral-600 sohne-mono">
              Detailed information and performance metrics
            </p>
          </div>
        </div>

        <!-- Student Info Card -->
        <div class="bg-white rounded-xl p-6 mb-6">
          <div class="flex items-start gap-6">
            <img
              :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(
                student.name
              )}&color=7F9CF5&background=EBF4FF&size=150`"
              :alt="student.name"
              class="rounded-xl w-[150px] h-[150px]"
            />

            <div class="flex flex-col gap-4">
              <div class="flex flex-col items-start gap-2">
                <h2 class="text-3xl font-semibold sohne">
                  {{ student.name }}
                </h2>
                <p class="text-[#7F9CF5] arame-mono">{{ student.email }}</p>
              </div>

              <div class="flex gap-6">
                <div class="flex flex-col gap-2">
                  <p class="text-neutral-600 text-sm sohne-mono">
                    Qualification
                  </p>
                  <span
                    class="px-3 py-1 bg-[#EBF4FF] rounded-full text-sm sohne-mono uppercase text-[#7F9CF5] text-center"
                  >
                    {{ student.qualification }}
                  </span>
                </div>

                <div class="flex flex-col gap-2">
                  <p class="text-neutral-600 text-sm sohne-mono">
                    Date of Birth
                  </p>
                  <p
                    class="px-3 py-1 bg-[#EBF4FF] rounded-full text-sm sohne-mono uppercase text-[#7F9CF5] text-center"
                  >
                    {{ student.dob }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="bg-white rounded-xl p-6">
            <h3 class="text-gray-500 text-sm sohne-mono mb-2">Total Quizzes</h3>
            <p class="text-3xl font-bold arame-mono">
              {{ student.quiz_stats.total_quizzes_attempted }}
            </p>
          </div>

          <div class="bg-white rounded-xl p-6">
            <h3 class="text-gray-500 text-sm sohne-mono mb-2">Last Active</h3>
            <p class="text-3xl font-bold arame-mono">
              {{ formatDate(student.quiz_stats.last_active) }}
            </p>
          </div>

          <div class="bg-white rounded-xl p-6">
            <h3 class="text-gray-500 text-sm sohne-mono mb-2">Average Score</h3>
            <div class="flex items-center gap-4">
              <p class="text-3xl font-bold arame-mono">
                {{ student.quiz_stats.performance_percentage }}%
              </p>
              <div class="flex-1">
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    class="h-2.5 rounded-full"
                    :class="[
                      student.quiz_stats.performance_percentage >= 70
                        ? 'bg-green-600'
                        : student.quiz_stats.performance_percentage >= 40
                        ? 'bg-yellow-400'
                        : 'bg-red-600',
                    ]"
                    :style="`width: ${student.quiz_stats.performance_percentage}%`"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl p-6 mb-6">
          <h3 class="text-xl font-semibold sohne-mono mb-4">Recent Activity</h3>
          <table class="w-full border-collapse">
            <thead>
              <tr
                class="text-left text-[#7F9CF5] sm:text-sm text-xs border-b-2 border-black"
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
                v-for="quiz in recentQuizzes"
                :key="quiz.id"
              >
                <td class="p-2">{{ quiz.quiz_name }}</td>
                <td class="p-2">{{ quiz.marks_scored }}</td>
                <td class="p-2 sm:block hidden">{{ quiz.percentage }}%</td>
                <td class="p-2">{{ formatDate(quiz.completed_at) }}</td>
                <td class="text-right">
                  <button
                    class="text-[#7F9CF5] hover:font-bold sm:text-sm text-xs sohne-mono bg-[#EBF4FF] sm:px-5 sm:py-1 py-[4px] rounded-md"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Performance Chart could be added here -->
      </template>
    </div>
  </Sidebar>
</template>

<style scoped>
.arame-mono {
  font-family: Inter;
  font-weight: 600;
  font-size: 16px;
}
</style>
