<template>
  <div>
    <div class="absolute top-6">
      <div class="w-[450px]">
        <SearchBar @search="handleSearch" placeholder="Search chapters..." />
      </div>
    </div>

    <div>
      <!-- Subject Header -->
      <div class="flex items-start gap-8 my-8">
        <img
          :src="subject?.image"
          :alt="subject?.name"
          class="w-[150px] h-[150px] rounded-xl object-cover"
        />
        <div>
          <h1 class="text-4xl font-bold mb-2 magnetic">{{ subject?.name }}</h1>
          <p class="text-gray-600 max-w-xl">{{ subject?.description }}</p>
          <p class="text-gray-600 mb-4">{{ subject?.chapters }} Chapters</p>
        </div>
      </div>
      <!-- Chapters Table -->
      <div>
        <div>
          <h2
            class="text-5xl font-semibold sohne tracking-[-1px] mb-4 magnetic"
          >
            Chapters
          </h2>
        </div>
        <div class="px-2">
          <table class="w-full chapters">
            <thead>
              <tr class="text-left text-sm border-b-2 border-black">
                <th>Chapter Name</th>
                <th>Description</th>
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
                class="border-b border-black"
              >
                <td class="py-2">
                  ▞ &nbsp;<span class="hover:text-[#0000ff]">{{
                    chapter.name
                  }}</span>
                </td>

                <td class="py-2">{{ chapter.description }}</td>
                <td class="py-2">
                  {{ chapter.quizzes || 0 }}
                </td>
                <td class="p-2 text-right">
                  <button
                    class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400 link-hover"
                  >
                    View
                  </button>
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

const route = useRoute();
const router = useRouter();
const isLoading = ref(false);
const subjectId = route.params.id;
const subject = ref(null);
const chapters = ref([]);
const searchQuery = ref("");

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
