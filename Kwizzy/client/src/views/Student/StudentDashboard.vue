<script setup>
import Sidebar from "@/components/Student/StudentSidebar.vue";
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const student = ref(null);
const isLoading = ref(true);
const student_id = parseInt(route.params.id);

// Mock data for recent quizzes (replace with actual API data)
const recentQuizzes = ref([
  {
    id: 1,
    name: "JavaScript Basics",
    score: 85,
    total: 100,
    date: "2024-01-05",
  },
  {
    id: 2,
    name: "Python Functions",
    score: 92,
    total: 100,
    date: "2024-01-04",
  },
  { id: 3, name: "Data Structures", score: 78, total: 100, date: "2024-01-03" },
]);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(student_id);
    console.log("student", student.value);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStudent();
});

// Computed properties for stats
const completionRate = computed(() => {
  if (!student.value) return 0;
  const stats = student.value.student_info.quiz_stats;
  return stats.total_quizzes_attempted > 0
    ? (stats.quizzes_completed / stats.total_quizzes_attempted) * 100
    : 0;
});

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

const stats = [
  { name: "AVERAGE SCORE", value: "75%", icon: "🎯" },
  { name: "QUIZZES COMPLETED", value: "24", icon: "📝" },
  { name: "ACTIVE STREAK", value: "7 days", icon: "🔥" },
  { name: "TOTAL TIME", value: "32hrs", icon: "⏱️" },
];

const recentActivity = [
  {
    id: 1,
    title: "Mathematics Quiz #3",
    timestamp: "2 hours ago",
    score: 85,
    icon: "📐",
  },
  {
    id: 2,
    title: "Science Quiz #5",
    timestamp: "1 day ago",
    score: 92,
    icon: "🧪",
  },
  {
    id: 3,
    title: "History Quiz #2",
    timestamp: "2 days ago",
    score: 68,
    icon: "📜",
  },
];
</script>

<template>
  <div class="min-h-screen">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <Loader />
    </div>

    <Sidebar v-else-if="student" :student="student">
      <div class="mb-10">
        <h2 class="text-4xl sohne-mono tracking-tight py-2">
          HELLO, {{ student.student_info.name }} ⚡️
        </h2>
        <p class="text-gray-500 sohne-mono text-sm">
          {{ getCurrentTimeGreeting() }} • {{ getCurrentDate() }}
        </p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        <div
          v-for="stat in stats"
          :key="stat.name"
          class="p-6 bg-[#fafafa] border border-gray-200 rounded-xl hover:-translate-y-1 transition-all duration-200"
        >
          <div class="flex items-center justify-between mb-4">
            <span class="text-2xl">{{ stat.icon }}</span>
            <span class="font-mono text-xs text-gray-500">{{ stat.name }}</span>
          </div>
          <p class="text-2xl font-bold font-mono">{{ stat.value }}</p>
          <p class="text-sm text-gray-500 font-mono">{{ stat.change }}</p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Recent Activity -->
        <div class="lg:col-span-2 space-y-6">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-mono">RECENT ACTIVITY</h3>
            <button
              class="text-sm font-mono hover:text-blue-600 transition-colors"
            >
              VIEW ALL +
            </button>
          </div>

          <div class="space-y-4">
            <div
              v-for="activity in recentActivity"
              :key="activity.id"
              class="p-4 bg-[#fafafa] border border-gray-200 rounded-lg hover:border-gray-300 transition-all duration-200"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="text-xl">{{ activity.icon }}</span>
                  <div>
                    <h4 class="font-mono text-sm">{{ activity.title }}</h4>
                    <p class="text-xs text-gray-500 font-mono">
                      {{ activity.timestamp }}
                    </p>
                  </div>
                </div>
                <span
                  class="text-sm font-mono px-2 py-1 rounded"
                  :class="[
                    activity.score >= 70
                      ? 'text-green-600 bg-green-50'
                      : 'text-orange-600 bg-orange-50',
                  ]"
                >
                  {{ activity.score }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="space-y-6">
          <div>
            <h3 class="text-xl font-mono mb-4">PERFORMANCE 📊</h3>
            <div class="p-6 bg-[#fafafa] border border-gray-200 rounded-xl">
              <div class="flex items-center justify-between mb-6">
                <div>
                  <p class="text-sm text-gray-500 font-mono">Average Score</p>
                  <p class="text-2xl font-bold font-mono"></p>
                </div>
                <div
                  class="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center"
                >
                  🎯
                </div>
              </div>
              <!-- Progress bars -->
              <div class="space-y-4">
                <div v-for="subject in subjects" :key="subject.name">
                  <div class="flex justify-between text-sm font-mono mb-1">
                    <span>{{ subject.name }}</span>
                    <span>{{ subject.progress }}%</span>
                  </div>
                  <div class="h-2 bg-gray-200 rounded-full">
                    <div
                      class="h-full rounded-full transition-all duration-300"
                      :style="{ width: `${subject.progress}%` }"
                      :class="subject.color"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Upcoming Quizzes -->
          <div>
            <h3 class="text-xl font-mono mb-4">UPCOMING QUIZZES 📝</h3>
            <div class="space-y-3">
              <div
                v-for="quiz in upcomingQuizzes"
                :key="quiz.id"
                class="p-4 bg-[#fafafa] border border-gray-200 rounded-lg hover:border-gray-300 transition-all duration-200"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-mono text-sm">{{ quiz.subject }}</h4>
                    <p class="text-xs text-gray-500 font-mono">
                      {{ quiz.date }}
                    </p>
                  </div>
                  <span class="text-xl">{{ quiz.icon }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Sidebar>
  </div>
</template>

<style scoped>
.font-mono {
  font-family: "SF Mono", SFMono-Regular, ui-monospace, "DejaVu Sans Mono",
    Menlo, Consolas, monospace;
}
</style>
