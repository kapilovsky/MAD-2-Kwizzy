<script setup>
import { ref, onMounted, useTemplateRef, onUnmounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import logo from "@/assets/images/landing-page/white logo.png";

const route = useRoute();
const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL;
const headerRef = useTemplateRef("headerRef");

const isLoading = ref(true);
const quiz = ref(null);
const subjectName = ref(null);
const chapterName = ref(null);


const quizId = route.params.quizId;

const fetchData = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    // Fetch all data concurrently
    const [quizRes, subjectRes, chapterRes] = await Promise.all([
      axios.get(`${API_URL}/quizzes/${quizId}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
    //   axios.get(`${API_URL}/subject/${subjectId}`, {
    //     headers: { Authorization: `Bearer ${token}` },
    //   }),
    //   axios.get(`${API_URL}/chapter/${chapterId}`, {
    //     headers: { Authorization: `Bearer ${token}` },
    //   }),
    ]);

    quiz.value = quizRes.data;
    // subjectName.value = subjectRes.data.name;
    // chapterName.value = chapterRes.data.name;
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};

const scrollToTop = () => {
  headerRef.value?.scrollIntoView({ behavior: "smooth", block: "start" });
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <header
      ref="headerRef"
      class="h-16 bg-white flex items-center justify-between gap-6 mb-2"
    >
      <div ref="topMarker" class="flex items-center flex-1">
        <div class="flex-1 max-w-lg">
          <h2 class="text-3xl font-bold sohne-mono">
            <span class="text-[34px]">🡲</span> Quiz Details
          </h2>
        </div>
      </div>

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

    <div class="py-4 px-4">
      <!-- Breadcrumbs -->
      <!-- <div class="flex items-center gap-2 text-sm mb-6">
        <RouterLink
          to="/admin"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          Subjects
        </RouterLink>
        <span class="text-gray-500">/</span>
        <RouterLink
          :to="`/admin/subject/${subjectId}`"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          {{ subjectName }}
        </RouterLink>
        <span class="text-gray-500">/</span>
        <RouterLink
          :to="`/admin/subject/${subjectId}/chapter/${chapterId}`"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          {{ chapterName }}
        </RouterLink>
        <span class="text-gray-500">/</span>
        <span class="text-black sohne-mono font-bold">{{ quiz?.name }}</span>
      </div> -->

      <!-- Quiz Details -->
      <div class="space-y-8">
        <!-- Quiz Info Card -->
        <div class="bg-[#192227] text-[#fdfcfc] p-6 rounded-2xl shadow">
          <div class="flex justify-between">
            <div class="space-y-4">
              <div>
                <h1 class="text-3xl font-bold">{{ quiz?.name }}</h1>
                <p class="text-gray-300 mt-2">{{ quiz?.description }}</p>
              </div>
              <div class="flex gap-8">
                <div>
                  <span class="text-gray-400 sohne-mono text-sm">Duration</span>
                  <p class="text-xl font-semibold">
                    {{ quiz?.time_duration }}
                  </p>
                </div>
                <div>
                  <span class="text-gray-400 sohne-mono text-sm">Price</span>
                  <p class="text-xl font-semibold">
                    {{ quiz?.price ? `₹${quiz.price}` : "Free" }}
                  </p>
                </div>
                <div>
                  <span class="text-gray-400 sohne-mono text-sm"
                    >Questions</span
                  >
                  <p class="text-xl font-semibold">
                    {{ quiz?.questions?.length || 0 }}
                  </p>
                </div>
              </div>
            </div>
            <div class="text-[160px] mt-[-40px] mb-[-40px]">🡽</div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end gap-4">
          <button
            @click="scrollToTop"
            class="px-6 py-2 border-2 border-[#192227] text-[#192227] rounded-lg hover:bg-gray-100 sohne-mono font-bold"
          >
            Back to Top
          </button>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<style scoped>
.shadow {
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}
</style>
