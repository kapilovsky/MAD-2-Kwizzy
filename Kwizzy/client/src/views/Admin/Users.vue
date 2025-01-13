<script setup>
import { ref, onMounted, watch } from "vue";
import { studentService } from "@/services/studentService";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import SearchIcon from "@/assets/images/icons/search.svg";
import SortIcon from "@/assets/images/icons/sort.svg";
import FilterIcon from "@/assets/images/icons/filter.svg";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import user from "@/assets/images/icons/user.svg";
import logo from "@/assets/images/landing-page/white logo.png";
import { useToast } from "@/composables/useToast";
const toast = useToast();

const students = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const currentPage = ref(1);
const totalPages = ref(0);
const totalStudents = ref(0);
const selectedSort = ref("name");
const sortOrder = ref("asc");
const itemsPerPage = ref(10);
const isExporting = ref(false);
const exportStatus = ref(null);
const taskId = ref(null);
const error = ref(null);

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
      `${API_URL}/export/admin-csv`,
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
        `${API_URL}/export/admin-csv?task_id=${taskId.value}`,
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

// Debounce search
let searchTimeout;
const handleSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    fetchStudents();
  }, 300);
};

// Watch for changes
watch([searchQuery, currentPage, selectedSort, sortOrder], () => {
  fetchStudents();
});

const fetchStudents = async () => {
  try {
    loading.value = true;
    const response = await studentService.getStudents({
      page: currentPage.value,
      per_page: itemsPerPage.value,
      search: searchQuery.value,
      sort_by: selectedSort.value,
      order: sortOrder.value,
    });
    students.value = response.students;
    totalPages.value = response.pages;
    totalStudents.value = response.total;
  } catch (error) {
    console.error("Error fetching students:", error);
  } finally {
    loading.value = false;
  }
};

const toggleSort = (field) => {
  if (selectedSort.value === field) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    selectedSort.value = field;
    sortOrder.value = "asc";
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

onMounted(() => {
  fetchStudents();
});
</script>

<template>
  <Sidebar>
    <!-- Header Section -->
    <div class="h-16 bg-white flex items-center justify-between px-6 mb-2">
      <div class="flex items-center gap-4 max-w-xl w-full">
        <div class="relative w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search students..."
            class="pl-10 pr-4 py-2 border border-gray-200 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-black"
            @input="handleSearch"
          />
          <component
            :is="SearchIcon"
            class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
          />
        </div>

        <button class="p-2 hover:bg-gray-100 rounded-lg">
          <component :is="FilterIcon" class="w-5 h-5" />
        </button>
      </div>
      <div>
        <div class="flex items-center gap-4">
          <img
            :src="logo"
            alt="User avatar"
            class="w-8 h-8 rounded-full mix-blend-exclusion"
          />
          <span class="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="px-6">
      <!-- Stats Cards -->
      <h1 class="text-4xl font-bold sohne mb-4">Users</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white flex items-center gap-6">
          <div class="text-sm text-gray-900 mb-2 sohne-mono">
            🡲 Total Students: {{ totalStudents }}
          </div>
          <button
            @click="exportCSV"
            :disabled="isExporting"
            class="text-sm hover:text-[#0000ff] text-gray-900 mb-2 sohne-mono"
          >
            🡲 {{ isExporting ? "Exporting..." : "[Export CSV]" }}
          </button>
        </div>
      </div>

      <!-- Table Section -->
      <div class="bg-white rounded-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b-2 border-gray-900">
                <th
                  v-for="header in [
                    'Name',
                    'Email',
                    'Qualification',
                    'DOB',
                    'Performance',
                  ]"
                  :key="header"
                  class="px-3 text-left font-medium text-gray-900"
                  @click="toggleSort(header.toLowerCase())"
                >
                  <div
                    class="flex py-[2px] items-center text-sm sohne-mono font-bold gap-2 cursor-pointer group"
                  >
                    {{ header }}
                    <component
                      :is="SortIcon"
                      class="w-5 h-5 opacity-0 group-hover:opacity-100"
                      :class="{
                        'opacity-100': selectedSort === header.toLowerCase(),
                        'rotate-180':
                          sortOrder === 'desc' &&
                          selectedSort === header.toLowerCase(),
                      }"
                    />
                  </div>
                </th>
                <th
                  class="px-3 text-sm text-right sohne-mono font-bold text-gray-900"
                >
                  Actions
                </th>
              </tr>
            </thead>

            <tbody class="divide-y">
              <template v-if="!loading">
                <tr
                  v-for="student in students"
                  :key="student.id"
                  class="hover:bg-[#fefff4] transition-colors duration-200"
                >
                  <td class="px-3 py-1">
                    <div class="flex items-center gap-3">
                      <img
                        v-if="student.profile_pic"
                        :src="student.profile_pic"
                        :alt="student.name"
                        class="w-8 h-8 rounded-full object-cover"
                      />
                      <img
                        v-else
                        :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(
                          student.name
                        )}&color=7F9CF5&background=EBF4FF`"
                        :alt="student.name"
                        class="w-8 h-8 rounded-full object-cover"
                      />

                      <div>
                        <div class="font-medium text-gray-900 arame-mono">
                          {{ student.name }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="px-3 py-1 text-gray-900 arame-mono">
                    {{ student.email }}
                  </td>
                  <td class="px-3 py-4">
                    <span
                      class="px-3 py-1 bg-[#EBF4FF] rounded-full text-sm sohne-mono uppercase text-[#7F9CF5]"
                    >
                      {{ student.qualification }}
                    </span>
                  </td>
                  <td class="px-3 py-1 text-gray-900">
                    {{ formatDate(student.dob) }}
                  </td>
                  <td class="px-3 py-1">
                    <div class="flex items-center gap-2">
                      <div
                        class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700"
                      >
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
                      <span class="text-sm text-gray-900 arame-mono">
                        {{ student.quiz_stats.performance_percentage }}%
                      </span>
                    </div>
                  </td>
                  <td class="px-3 py-1 text-right">
                    <RouterLink
                      :to="`/admin/student/${student.id}`"
                      class="text-[#7F9CF5] bg-[#EBF4FF] hover:text-[#0000ff] transition-all duration-200 px-3 py-1 rounded sohne-mono text-sm"
                    >
                      View Details
                    </RouterLink>
                  </td>
                </tr>
              </template>

              <tr v-else>
                <td colspan="6" class="px-6 py-8 text-center">
                  <Loader />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="px-3 py-2 bg-[#fefff0] flex items-center justify-between">
          <div class="text-sm sohne text-neutral-500">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
            {{ Math.min(currentPage * itemsPerPage, totalStudents) }} of
            {{ totalStudents }} students
          </div>

          <div class="flex items-center gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed sohne"
            >
              Previous
            </button>

            <div class="flex items-center gap-1">
              <button
                v-for="page in totalPages"
                :key="page"
                @click="currentPage = page"
                class="w-8 h-8 flex items-center justify-center rounded"
                :class="
                  currentPage === page
                    ? 'bg-blue-600 text-white'
                    : 'hover:bg-gray-100'
                "
              >
                {{ page }}
              </button>
            </div>

            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed sohne"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<style scoped>
/* Add any additional styles here */
.arame-mono {
  font-family: Inter;
  font-weight: 600;
  font-size: 16px;
}
</style>
