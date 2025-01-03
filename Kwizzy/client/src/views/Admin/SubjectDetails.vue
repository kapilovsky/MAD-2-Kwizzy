<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import "../../assets/font.css";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import Sidebar from "@/components/Admin/Sidebar.vue";
import AddChapter from "@/components/Admin/AddChapter.vue";

const route = useRoute();
const router = useRouter();
const subjectId = route.params.id;
const subject = ref(null);
const chapters = ref([]);
const isAddChapterModalOpen = ref(false);

const fetchSubjectDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/subject/${route.params.id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    subject.value = {
      ...response.data,
      image: `${API_URL}/uploads/subjects/${response.data.subject_image}`,
    };
    console.log("Fetched subject details:", subject.value);
    chapters.value = response.data.chapters || [];
  } catch (error) {
    console.error("Error fetching subject details:", error);
  }
};

const fetchChapters = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(`${API_URL}/chapter`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: { subject_id: subjectId },
    });

    console.log("Full response data:", response.data);
    chapters.value = response.data.chapters || [];
  } catch (error) {
    console.error("Error fetching subject details:", error);
  }
};

const handleChapterCreated = (chapter) => {
  chapters.value.push(chapter);
  isAddChapterModalOpen.value = false;
};

onMounted(() => {
  fetchSubjectDetails();
  fetchChapters();
});
</script>

<template>
  <Sidebar>
    <!-- Breadcrumbs -->
    <div class="flex items-center gap-2 text-sm mb-6">
      <router-link
        to="/admin"
        class="text-gray-500 hover:text-black sohne-mono"
      >
        Subjects
      </router-link>
      <span class="text-gray-500">/</span>
      <span class="font-medium sohne-mono">{{ subject?.name }}</span>
    </div>

    <!-- Subject Header -->
    <div class="flex items-start gap-6 mb-8">
      <img
        :src="subject?.image"
        :alt="subject?.name"
        class="w-[150px] h-[150px] rounded-xl object-cover"
      />
      <div>
        <h1 class="text-4xl font-bold mb-2">{{ subject?.name }}</h1>
        <p class="text-gray-600">{{ subject?.description }}</p>
        <p class="text-gray-600 mb-4">{{ subject?.chapters }} Chapters</p>
        <button
          @click="isAddChapterModalOpen = true"
          class="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          Add Chapter
        </button>
      </div>
    </div>
    <!-- Chapters Table -->
    <div>
      <div>
        <h2 class="text-6xl font-semibold sohne tracking-[-2px] mb-4">
          Chapters
        </h2>
      </div>
      <div class="px-2">
        <table class="w-full">
          <thead>
            <tr class="text-left text-sm border-b-2 border-black">
              <th>Chapter Name</th>
              <th>Description</th>
              <th>Quizzes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="chapters.length === 0">
              <td colspan="4" class="py-4 text-center sohne text-gray-500">
                No chapters found. Add your first chapter!
              </td>
            </tr>
            <tr
              v-for="chapter in chapters"
              :key="chapter.id"
              class="border-b border-black"
            >
              <td class="py-2">{{ chapter.name }}</td>
              <td class="py-2">{{ chapter.description }}</td>
              <td class="py-2">
                {{ chapter.quizzes || 0 }}
              </td>
              <td class="py-2">
                <div class="flex items-center gap-2">
                  <button
                    @click="editChapter(chapter)"
                    class="p-1 text-gray-600 hover:text-black"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    @click="deleteChapter(chapter.id)"
                    class="p-1 text-gray-600 hover:text-red-600"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Chapter Modal (create a separate component for this) -->
    <AddChapter
      v-if="isAddChapterModalOpen"
      :is-open="isAddChapterModalOpen"
      :subject-id="route.params.id"
      @close="isAddChapterModalOpen = false"
      @create="handleChapterCreated"
    />
  </Sidebar>
</template>

<style scoped>
.sohne {
  font-family: sohne;
}

.sohne-mono {
  font-family: sohne-mono;
  text-transform: uppercase;
}

table th {
  font-family: sohne-mono;
  text-transform: uppercase;
}
table td {
  font-family: sohne-mono;
  font-size: 18px;
  letter-spacing: -0.6px;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  background-color: #f0f0ff;
}
</style>
