<!-- views/Student/StudentLayout.vue -->
<template>
  <div class="min-h-screen">
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <Loader />
    </div>

    <StudentSidebar v-else-if="student" :student="student">
      <router-view v-slot="{ Component }">
        <component :is="Component" :student="student" />
      </router-view>
    </StudentSidebar>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import StudentSidebar from "@/components/Student/StudentSidebar.vue";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const student = ref(null);
const isLoading = ref(true);

const fetchStudent = async () => {
  try {
    isLoading.value = true;
    student.value = await studentService.getStudent(parseInt(route.params.id));
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
