<script setup>
import { useRoute, RouterLink } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import arrow from "../../assets/images/icons/Arrow.png";
import check from "../../assets/images/icons/check.svg";
import EditProfile from "@/components/Student/EditProfile.vue";
import { useToast } from "@/composables/useToast";
const toast = useToast();

const route = useRoute();
const isLoading = ref(true);
const error = ref(null);
const recentQuizzes = ref([]);
const isEditProfileModalOpen = ref(false);
const isExporting = ref(false);
const exportStatus = ref(null);
const taskId = ref(null);

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const exportCSV = async () => {
  try {
    isExporting.value = true;
    exportStatus.value = "processing";
    toast.info(
      "Generating your export. You will receive the download link via email..."
    );
    error.value = null;
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("Token not found");
    }

    const response = await axios.post(
      `${API_URL}/export/user-csv`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    taskId.value = response.data.task_id;

    await pollExportStatus();
  } catch (err) {
    error.value = "Failed to start export. Please try again.";
    console.error("Export error:", err);
  }
};

const pollExportStatus = async () => {
  try {
    const token = localStorage.getItem("access_token");

    while (true) {
      const response = await axios.get(
        `${API_URL}/export/user-csv?task_id=${taskId.value}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (
        response.data.status === "SUCCESS" &&
        response.data.result.status === "success"
      ) {
        toast.success(
          "Export completed! Check your email for the download link."
        );

        break;
      } else if (
        response.data.status === "FAILURE" ||
        (response.data.status === "SUCCESS" &&
          response.data.result.status === "error")
      ) {
        throw new Error(response.data.result.message || "Export failed");
      }

      await new Promise((resolve) => setTimeout(resolve, 2000));
    }
  } catch (err) {
    exportStatus.value = "error";
    toast.error("Failed to generate export. Please try again.");
    console.error("Polling error:", err);
  } finally {
    isExporting.value = false;
  }
};

const fetchStudentData = async () => {
  try {
    isLoading.value = true;

    const response = await studentService.getStudent(
      props.student.student_info.id
    );
    student.value = response;
  } catch (error) {
    console.error("Error fetching student data:", error);
  } finally {
    isLoading.value = false;
  }
};

const openEditModal = () => {
  isEditProfileModalOpen.value = true;
};

const student = ref(props.student);

const getRecentActivity = async () => {
  try {
    isLoading.value = true;
    recentQuizzes.value = await studentService.getRecentActivity(
      props.student.student_info.id
    );
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

const getCurrentTimeGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 18) return "Good Afternoon";
  return "Good Evening";
};

const getCurrentDate = () => {
  return new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const handleProfileUpdated = (updatedStudent) => {
  student.value = updatedStudent;
  isEditProfileModalOpen.value = false;
  fetchStudentData();
};

onMounted(() => {
  getRecentActivity();
  // console.log("student ", student.value);
  console.log("student from service", student.value);
});
</script>

<template>
  <div>
    <div class="mb-10 flex gap-4">
      <div class="relative overflow-hidden">
        <div
          v-if="!student.student_info.profile_pic"
          class="sm:w-40 sm:h-40 w-0 h-0 rounded-lg bg-[#192227] text-white/20 hover:text-white/40 transition-all duration-200"
        >
          <span class="absolute -bottom-6 right-0 text-9xl">{{
            student.student_info.name.charAt(0)
          }}</span>
        </div>
        <div v-else>
          <img
            :src="student.student_info.profile_pic"
            alt="Profile Picture"
            class="sm:w-40 sm:h-40 w-0 h-0 rounded-lg"
          />
        </div>
      </div>
      <div>
        <h2 class="text-4xl sohne-mono tracking-tight py-2 font-bold">
          HELLO, {{ student.student_info.name }}✨
        </h2>
        <p class="text-neutral-600 sohne-mono text-sm">
          {{ getCurrentTimeGreeting() }} • {{ getCurrentDate() }}
        </p>
        <div class="flex gap-4">
          <button
            class="sohne-mono text-xs text-neutral-600 mt-2 uppercase hover:text-[#0000ff]"
            @click="openEditModal"
          >
            [Edit Profile]
          </button>
          <button
            class="sohne-mono text-xs text-neutral-600 mt-2 uppercase hover:text-[#0000ff]"
            @click="exportCSV"
            :disabled="isExporting"
          >
            {{ isExporting ? "Exporting..." : "[Export CSV]" }}
          </button>
        </div>
        <div class="font-mono text-xs text-gray-400 mt-2 uppercase">
          {{ student.student_info.email }}
        </div>
        <div class="font-mono text-xs text-gray-400 mt-1 uppercase">
          {{ student.student_info.qualification }}
        </div>
        <div class="font-mono text-xs text-gray-400 mt-1">
          ID: #{{ student.student_info.id.toString().padStart(4, "0") }}
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- Performance Card -->
      <div
        class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#192227] overflow-hidden relative group"
      >
        <div
          class="absolute -top-10 -right-32 opacity-10 group-hover:opacity-20 transition-all duration-200"
        >
          <img :src="arrow" class="w-[70%]" alt="" />
        </div>
        <h3
          class="font-mono font-medium uppercase text-sm tracking-wider text-[#e0f2ff] mb-4"
        >
          Performance
        </h3>
        <div
          class="text-5xl sohne font-bold bg-gradient-to-r from-[#e0f2ff] bg-clip-text text-transparent"
        >
          {{ student.student_info.quiz_stats.performance_percentage }}%
        </div>
        <p class="sohne-mono text-xs text-[#e0f2ff]/70 mt-2 uppercase">
          Keep up the good work
        </p>
      </div>

      <!-- Activity Card -->
      <div
        class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#fff9f0] overflow-hidden relative group"
      >
        <div
          class="absolute -top-40 -right-40 text-[340px] opacity-10 group-hover:opacity-30 transition-all duration-300"
        >
          ⚡️
        </div>
        <h3
          class="font-mono font-medium uppercase text-sm tracking-wider text-orange-600 mb-4"
        >
          Last Active
        </h3>
        <div class="sm:text-5xl text-4xl sohne font-bold text-orange-600">
          {{ formatDate(student.student_info.quiz_stats.last_active) }}
        </div>
        <p class="font-mono text-xs text-orange-500 mt-2 uppercase">
          Keep the momentum
        </p>
      </div>
      <div
        class="rounded-3xl p-8 shadow-sm transition-all hover:shadow-lg bg-[#192227] overflow-hidden relative group"
      >
        <div
          class="absolute -top-24 -right-16 text-6xl opacity-10 group-hover:opacity-30 transition-all duration-300"
        >
          <component :is="check" class="fill-[#fff] w-[400px] h-[400px]" />
        </div>
        <h3
          class="font-mono font-medium uppercase text-sm tracking-wider text-[#f0f7ff] mb-4"
        >
          Completed
        </h3>
        <div
          class="text-5xl sohne font-bold bg-gradient-to-r from-[#e0f2ff] bg-clip-text text-transparent"
        >
          {{ student.student_info.quiz_stats.total_quizzes_attempted }}
        </div>
        <p class="font-mono text-xs text-[#f0f7ff]/70 mt-2 uppercase">
          quizzes attempted
        </p>
      </div>
    </div>

    <!-- Recent Activity -->
    <div
      class="rounded-3xl sm:px-8 px-4 py-6 shadow-sm transition-all hover:shadow-lg bg-[#fff9f0]"
    >
      <div class="flex items-center justify-between mb-6">
        <h3
          class="font-bold sm:text-[48px] text-3xl text-orange-600 tracking-tighter"
        >
          Recent Activity
        </h3>
        <RouterLink :to="`${route.path}/quiz/history`">
          <span class="sm:text-sm text-xs text-orange-600 sohne-mono font-bold"
            >+ VIEW MORE</span
          >
        </RouterLink>
      </div>
      <table class="w-full border-collapse">
        <thead>
          <tr
            class="text-left text-orange-600 sm:text-sm text-xs border-b-2 border-black"
          >
            <th class="p-2">Quiz Title</th>
            <th class="p-2">Score</th>
            <th class="p-2 sm:table-cell hidden">Accuracy</th>
            <th class="p-2 sm:table-cell hidden">Completion Date</th>
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
            <td class="p-2 sm:table-cell hidden">{{ quiz.percentage }}%</td>
            <td class="p-2 sm:table-cell hidden">
              {{ formatDate(quiz.completed_at) }}
            </td>
            <td class="text-right p-2">
              <RouterLink
                :to="{
                  name: 'quiz-results',
                  params: {
                    id: route.params.id,
                    quizId: quiz.quiz_id,
                  },
                  query: {
                    resultId: quiz.quiz_result_id,
                  },
                }"
                class="text-orange-500 hover:font-bold sm:text-sm text-xs sohne-mono bg-orange-200 sm:px-5 px-[6px] py-1 rounded-md text-nowrap"
              >
                View Details
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <EditProfile
      v-if="isEditProfileModalOpen"
      :is-open="isEditProfileModalOpen"
      :student="student.student_info"
      @close="isEditProfileModalOpen = false"
      @update="handleProfileUpdated"
    />
  </div>
</template>

<style scoped>
.font-mono {
  font-family: "IBM Plex Mono";
}

tbody tr {
  transition: all 0.15s ease;
}

tbody tr:hover {
  background-color: #ffecd0;
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
