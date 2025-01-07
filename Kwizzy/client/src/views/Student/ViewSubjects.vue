<template>
  <div>
    <div class="mb-6 mt-4">
      <h1 class="text-4xl font-bold">Subjects</h1>
      <p>
        Explore a variety of subjects and choose the ones you want to practice.
      </p>
    </div>
    <SubjectCard
      :subjects="filteredSubjects"
      :loading="subjectStore.isLoading"
    />
  </div>
</template>
<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, computed } from "vue";
import { useSubjectStore } from "@/stores/subjectStore";
const subjectStore = useSubjectStore();
import SearchBar from "../../components/Admin/SearchBar.vue";
import SubjectCard from "@/components/Student/SubjectCard.vue";

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const searchQuery = ref("");

const filteredSubjects = computed(() => {
  if (!searchQuery.value) return subjectStore.allSubjects;

  const query = searchQuery.value.toLowerCase();
  return subjectStore.allSubjects.filter(
    (subject) =>
      subject.name.toLowerCase().includes(query) ||
      subject.description.toLowerCase().includes(query)
  );
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

const student = ref(props.student);

onMounted(() => {
  subjectStore.fetchSubjects();
});
</script>
