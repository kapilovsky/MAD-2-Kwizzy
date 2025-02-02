<!-- components/Admin/Search.vue -->
<script setup>
import { ref } from "vue";
import SearchIcon from "../../assets/images/icons/search.svg";

defineProps({
  placeholder: {
    type: String,
    default: "Search...",
  },
});

const emit = defineEmits(["search"]);

const searchQuery = ref("");

const handleSearch = () => {
  emit("search", searchQuery.value.toLowerCase());
};
</script>

<template>
  <div class="relative sm:ml-0 ml-12">
    <component
      :is="SearchIcon"
      class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
    />
    <input
      v-model="searchQuery"
      type="text"
      :placeholder="placeholder"
      class="sm:w-full w-[220px] pl-10 sm:pr-4 py-2 bg-gray-100 text-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      @input="handleSearch"
    />
  </div>
</template>
