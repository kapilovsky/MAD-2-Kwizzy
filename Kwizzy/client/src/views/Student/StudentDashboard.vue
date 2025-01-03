<script setup>
import Sidebar from "@/components/Student/StudentSidebar.vue";
// get the access token from local storage
const access_token = localStorage.getItem("access_token");
console.log("access_token", access_token);
</script>

<template>
  <Sidebar>
    <h1>Student Dashboard</h1>
  </Sidebar>
</template>
