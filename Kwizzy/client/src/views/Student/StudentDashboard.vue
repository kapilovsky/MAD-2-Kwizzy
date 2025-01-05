<script setup>
import Sidebar from "@/components/Student/StudentSidebar.vue";
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted } from "vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import { useToast } from "@/composables/useToast";
const API_URL = import.meta.env.VITE_API_URL;

const route = useRoute();
const toast = useToast();
const student = ref(null);
const isLoading = ref(true);
const student_id = parseInt(route.params.id);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(student_id);
  } catch (error) {
    toast.error("Error fetching student data");
    console.error("Error:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStudent();
});
</script>

<template>
  <div>
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <Loader />
    </div>
    <Sidebar v-else-if="student" :student="student">
      <h1>Student Dashboard</h1>
    </Sidebar>

    <div v-else class="flex justify-center items-center min-h-screen">
      No student data found
    </div>
  </div>
</template>
