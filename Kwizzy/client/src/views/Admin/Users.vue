<!-- views/Admin/Users.vue -->
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

const students = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const currentPage = ref(1);
const totalPages = ref(0);
const totalStudents = ref(0);
const selectedSort = ref("name");
const sortOrder = ref("asc");
const itemsPerPage = ref(10);

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
    <div class="h-16 bg-white flex items-center justify-between px-6 mb-6">
      <h1 class="text-2xl font-bold">Users</h1>
      <div class="flex items-center gap-4">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search students..."
            class="pl-10 pr-4 py-2 border border-gray-200 rounded-lg w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
    </div>

    <!-- Main Content -->
    <div class="px-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-xl p-6 border border-gray-100">
          <div class="text-sm text-gray-500 mb-2">Total Students</div>
          <div class="text-2xl font-bold">{{ totalStudents }}</div>
        </div>
        <!-- Add more stat cards as needed -->
      </div>

      <!-- Table Section -->
      <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-100">
                <th
                  v-for="header in [
                    'Name',
                    'Email',
                    'Qualification',
                    'DOB',
                    'Performance',
                  ]"
                  :key="header"
                  class="px-6 py-4 text-left text-sm font-medium text-gray-500"
                  @click="toggleSort(header.toLowerCase())"
                >
                  <div class="flex items-center gap-2 cursor-pointer group">
                    {{ header }}
                    <component
                      :is="SortIcon"
                      class="w-4 h-4 opacity-0 group-hover:opacity-100"
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
                  class="px-6 py-4 text-right text-sm font-medium text-gray-500"
                >
                  Actions
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-100">
              <template v-if="!loading">
                <tr
                  v-for="student in students"
                  :key="student.id"
                  class="hover:bg-gray-50 transition-colors duration-200"
                >
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <img
                        v-if="student.profile_pic"
                        :src="student.profile_pic"
                        :alt="student.name"
                        class="w-8 h-8 rounded-full object-cover"
                      />
                      <component
                        v-else
                        :is="user"
                        class="w-8 h-8 rounded-full object-cover"
                      />

                      <div>
                        <div class="font-medium text-gray-900">
                          {{ student.name }}
                        </div>
                        <div class="text-sm text-gray-500">
                          ID: {{ student.id }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-gray-600">{{ student.email }}</td>
                  <td class="px-6 py-4">
                    <span class="px-2 py-1 bg-gray-100 rounded-full text-sm">
                      {{ student.qualification }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-gray-600">
                    {{ formatDate(student.dob) }}
                  </td>
                  <td class="px-6 py-4">
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
                      <span class="text-sm text-gray-600">
                        {{ student.quiz_stats.performance_percentage }}%
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <RouterLink
                      :to="`/admin/student/${student.id}`"
                      class="text-blue-600 hover:text-blue-800 font-medium text-sm"
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
        <div
          class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between"
        >
          <div class="text-sm text-gray-500">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
            {{ Math.min(currentPage * itemsPerPage, totalStudents) }} of
            {{ totalStudents }} students
          </div>

          <div class="flex items-center gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded border border-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
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
              class="px-3 py-1 rounded border border-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
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
</style>
