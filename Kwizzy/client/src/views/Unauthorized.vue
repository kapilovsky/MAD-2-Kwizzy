<!-- views/Unauthorized.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Unauthorized Access</h1>
      <p class="text-gray-600 mb-8">
        You don't have permission to access this page.
      </p>
      <button
        @click="goBack"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Go Back
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goBack = () => {
  const userRole = getUserRole();
  if (userRole === "student") {
    router.push("/student/" + getUserId());
  } else if (userRole === "admin") {
    router.push("/admin/dashboard");
  } else {
    router.push("/login");
  }
};
</script>
