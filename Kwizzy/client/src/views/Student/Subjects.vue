<template>
  <div v-if="isLoading">
    <Loader />
  </div>

  <!-- Show sidebar only when student data is available -->
  <StudentSidebar v-else-if="student" :student="student">
    <!-- BreadCrumbs -->
    <nav class="flex items-center text-sm font-medium text-gray-500 mt-4">
      <router-link :to="`/student/${student_id}`" class="hover:text-black"
        >Dashboard</router-link
      >
      <span>/</span>
      <span>Subjects</span>
    </nav>
    Subjects
  </StudentSidebar>

  <!-- Optional: Show error state -->
  <div v-else class="text-center p-4">
    <p>Unable to load student data</p>
  </div>
</template>
<script setup>
import StudentSidebar from "@/components/Student/StudentSidebar.vue";
import { useRoute, useRouter } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;

const route = useRoute();
const student = ref(null);
const isLoading = ref(true);
const subjects = ref([]);

const student_id = parseInt(route.params.id);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(student_id);
    console.log(student.value);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStudent();
});
</script>
