<template>
  <Loader v-if="isLoading" />
  <div v-else>
    <div class="absolute sm:top-6 top-16">
      <div class="sm:w-[450px] w-[300px]">
        <SearchBar @search="handleSearch" placeholder="Search chapters..." />
      </div>
    </div>

    <div class="sm:mt-4 mt-16">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-2 text-gray-600 text-sm">
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
        <span class="text-black sohne-mono">{{ subject?.name }}</span>
      </div>

      <!-- Subject Header -->
      <div
        class="flex flex-col sm:flex-row sm:items-center items-start gap-8 my-4"
      >
        <img
          :src="subject?.image"
          :alt="subject?.name"
          class="sm:w-[150px] sm:h-[150px] rounded-xl object-cover"
        />
        <div class="flex flex-col gap-2 justify-between">
          <h1 class="text-4xl font-bold">{{ subject?.name }}</h1>
          <p class="text-gray-600 max-w-xl text-lg">
            {{ subject?.description }}
          </p>
          <p class="text-gray-600">Total Chapters: {{ subject?.chapters }}</p>
          <p class="text-gray-600 mb-4">
            Total Students enrolled in this subject:
            {{ subject?.students }}
          </p>
        </div>
      </div>
      <!-- Chapters Table -->
      <div>
        <div>
          <h2
            class="sm:text-5xl text-3xl font-semibold sohne tracking-[-1px] mb-4"
          >
            Chapters
          </h2>
        </div>
        <div class="px-2">
          <table class="w-full">
            <thead>
              <tr class="text-left sm:text-sm text-xs border-b-2 border-black">
                <th>Chapter Name</th>
                <th class="sm:block hidden">Description</th>
                <th>Quizzes</th>
                <th class="text-right px-2">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="chapters.length === 0">
                <td colspan="4" class="py-4 text-center sohne text-gray-500">
                  No chapters found.
                </td>
              </tr>
              <tr
                v-for="chapter in filteredChapters"
                :key="chapter.id"
                class="border-b text-sm sm:text-base border-black hover:bg-[#fff9f0]"
              >
                <td class="py-2">
                  ▞ &nbsp;<span>{{ chapter.name }}</span>
                </td>

                <td class="py-2 sm:block hidden">{{ chapter.description }}</td>
                <td class="py-2">
                  {{ chapter.quizzes || 0 }}
                </td>
                <td class="p-2 text-right">
                  <RouterLink :to="`${route.path}/chapter/${chapter.id}`">
                    <button
                      class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400 link-hover"
                    >
                      View
                    </button>
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
import { useRoute, useRouter, RouterLink } from "vue-router";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import SearchBar from "@/components/Admin/SearchBar.vue";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const router = useRouter();
const isLoading = ref(false);
const subjectId = route.params.subjectId;
const subject = ref(null);
const chapters = ref([]);
const searchQuery = ref("");

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const student = ref(props.student);
const studentId = student.value.id;

const fetchSubjectDetails = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/subject/${subjectId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    subject.value = {
      ...response.data,
      image: `${API_URL}/uploads/subjects/${response.data.subject_image}`,
    };
  } catch (error) {
    console.error("Error fetching subject details:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchChapters = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/chapter`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: { subject_id: subjectId },
    });
    chapters.value = response.data.chapters || [];
  } catch (error) {
    console.error("Error fetching subject details:", error);
  } finally {
    isLoading.value = false;
  }
};

const filteredChapters = computed(() => {
  if (!searchQuery.value) {
    return chapters.value;
  }

  return chapters.value.filter(
    (chapter) =>
      chapter.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      chapter.description
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
  );
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

onMounted(() => {
  fetchSubjectDetails();
  fetchChapters();
});
</script>
