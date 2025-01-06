<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import "../../assets/font.css";
import logo from "../../assets/images/landing-page/white logo.png";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import Sidebar from "@/components/Admin/Sidebar.vue";
import EditSubject from "@/components/Admin/EditSubject.vue";
import AddChapter from "@/components/Admin/AddChapter.vue";
import EditChapter from "@/components/Admin/EditChapter.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";
import Loader from "@/components/Loader.vue";
import { RouterLink } from "vue-router";
import { useToast } from "@/composables/useToast";
import { useEventStore } from "@/composables/eventBus";
const eventStore = useEventStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();
const subjectId = route.params.id;
const subject = ref(null);
const chapters = ref([]);
const searchQuery = ref("");

const selectedChapter = ref(null);
const isAddChapterModalOpen = ref(false);
const isEditChapterModalOpen = ref(false);
const isEditSubjectModalOpen = ref(false);
const isLoading = ref(true);

const fetchSubjectDetails = async () => {
  try {
    isLoading.value = true;
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

const handleChapterCreated = (chapter) => {
  chapters.value.push(chapter);
  isAddChapterModalOpen.value = false;
};

const handleChapterUpdated = (updatedChapter) => {
  const index = chapters.value.findIndex(
    (chapter) => chapter.id === updatedChapter.id
  );
  if (index !== -1) {
    chapters.value[index] = updatedChapter; // Update the chapter in the array
  }
  isEditChapterModalOpen.value = false; // Close the edit modal
};

const handleSubjectUpdated = (updatedSubject) => {
  subject.value = {
    ...updatedSubject,
    image: `${API_URL}/uploads/subjects/${updatedSubject.subject_image}`,
  };
  console.log("Updated subject:", subject.value);
  isEditSubjectModalOpen.value = false;
  eventStore.triggerSubjectRefresh()
};

onMounted(() => {
  fetchSubjectDetails();
  fetchChapters();
});

const openEditModal = (chapter) => {
  selectedChapter.value = chapter;
  isEditChapterModalOpen.value = true;
};

const editSubject = (subject) => {
  isEditSubjectModalOpen.value = true;
};

const deleteSubject = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.delete(`${API_URL}/subject/${subjectId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    toast.success(response.data.message);
    router.push("/admin/dashboard");
  } catch (error) {
    console.error("Error deleting subject:", error);
  }
};

const deleteChapter = async (chapterId) => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.delete(`${API_URL}/chapter/${chapterId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    toast.success(response.data.message);
    fetchChapters();
  } catch (error) {
    console.error("Error deleting chapter:", error);
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
</script>

<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <header class="h-16 bg-white flex items-center justify-between gap-6 mb-2">
      <div class="flex items-center flex-1">
        <div class="flex-1 max-w-lg">
          <div class="relative">
            <SearchBar
              @search="handleSearch"
              placeholder="Search chapters..."
            />
          </div>
        </div>
      </div>

      <!-- Right Side Icons -->
      <div class="flex items-center">
        <div class="flex items-center gap-4">
          <img
            :src="logo"
            alt="User avatar"
            class="w-8 h-8 rounded-full mix-blend-difference"
          />
          <span class="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </header>
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
    <div class="flex items-start gap-8 mb-8">
      <img
        :src="subject?.image"
        :alt="subject?.name"
        class="w-[150px] h-[150px] rounded-xl object-cover"
      />
      <div>
        <h1 class="text-4xl font-bold mb-2 magnetic">{{ subject?.name }}</h1>
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
      <div class="flex items-start gap-[80px]">
        <button
          @click="editSubject(subject)"
          class="px-4 py-2 text-sm text-black rounded-lg hover:text-[#0000ff] transition-colors sohne-mono focus:outline-none"
        >
          <span class="relative">
            <sup class="absolute text-[12px] left-[-8px] sohne-mono">+</sup>
            Edit
            <sup class="absolute text-[10px] font-mono"> [Subject] </sup>
          </span>
        </button>
        <button
          @click="deleteSubject"
          class="px-4 py-2 text-sm text-black rounded-lg hover:text-[#ff0a0a] transition-colors sohne-mono"
        >
          <span class="relative">
            Delete
            <sup class="absolute text-[10px] font-mono"> [Subject]</sup>
            <sup class="absolute text-[12px] top-[20px] right-[-8px] sohne-mono"
              >+</sup
            >
          </span>
        </button>
      </div>
    </div>
    <!-- Chapters Table -->
    <div>
      <div>
        <h2 class="text-5xl font-semibold sohne tracking-[-1px] mb-4 magnetic">
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
              v-for="chapter in filteredChapters"
              :key="chapter.id"
              class="border-b border-black"
            >
              <RouterLink
                :to="`/admin/subject/${subject.id}/chapter/${chapter.id}`"
              >
                <td class="py-2">
                  ▞ &nbsp;<span class="hover:text-[#0000ff]">{{
                    chapter.name
                  }}</span>
                </td>
              </RouterLink>

              <td class="py-2">{{ chapter.description }}</td>
              <td class="py-2">
                {{ chapter.quizzes || 0 }}
              </td>
              <td class="py-2">
                <div class="flex items-center gap-2">
                  <button
                    @click="openEditModal(chapter)"
                    class="py-[2px] px-1 text-gray-600 hover:text-[#0000ff] sohne-mono text-[12px] border-dotted border border-gray-400 link-hover"
                  >
                    EDIT
                  </button>
                  <button
                    @click="deleteChapter(chapter.id)"
                    class="py-[2px] px-1 text-gray-600 hover:text-red-600 sohne-mono text-[12px] border-dotted border border-gray-400 link-hover"
                  >
                    DELETE
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Subject Modal (create a separate component for this) -->
    <EditSubject
      v-if="isEditSubjectModalOpen"
      :is-open="isEditSubjectModalOpen"
      :subject="{
        ...subject,
        subject_image: subject.subject_image,
      }"
      @close="isEditSubjectModalOpen = false"
      @update="handleSubjectUpdated"
    />

    <!-- Add Chapter Modal (create a separate component for this) -->
    <AddChapter
      v-if="isAddChapterModalOpen"
      :is-open="isAddChapterModalOpen"
      :subject-id="route.params.id"
      :subject-name="subject.name"
      @close="isAddChapterModalOpen = false"
      @create="handleChapterCreated"
    />

    <!-- Edit Chapter Modal (create a separate component for this) -->
    <EditChapter
      v-if="isEditChapterModalOpen"
      :is-open="isEditChapterModalOpen"
      :subject-id="route.params.id"
      :subject-name="subject.name"
      :chapter="selectedChapter"
      @close="isEditChapterModalOpen = false"
      @update="handleChapterUpdated"
    />
  </Sidebar>
</template>

<style>
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
table td,
table td span {
  font-family: monospace;
  font-size: 18px;
  letter-spacing: -0.6px;
}

tbody tr {
  transition: all 0.15s ease;
}

tbody tr:hover {
  background-color: #f0f0ff;
}
</style>
