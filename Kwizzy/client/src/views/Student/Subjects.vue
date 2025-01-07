<template>Subjects</template>
<script setup>
import { useRoute } from "vue-router";
import { studentService } from "@/services/studentService";
import { ref, onMounted, computed } from "vue";

const route = useRoute();
const isLoading = ref(true);
const recentQuizzes = ref([]);

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const student = ref(props.student);
</script>
