<!-- components/CreateSubjectModal.vue -->
<script setup>
import { ref } from "vue";

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close", "create"]);

const modalRef = ref(null);
const subjectData = ref({
  name: "",
  description: "",
  image: null,
});

const handleSubmit = () => {
  emit("create", subjectData.value);
  subjectData.value = { name: "", description: "", image: null };
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    subjectData.value.image = file;
  }
};
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <!-- Backdrop -->
      <div
        class="absolute inset-0 bg-black/20 backdrop-blur-sm"
        @click="$emit('close')"
      ></div>

      <!-- Modal -->
      <Transition name="slideUp">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div
            ref="modalRef"
            class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-[500px] p-6 relative z-10"
            @click.stop
          >
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Create New Subject
            </h2>

            <form @submit.prevent="handleSubmit" class="space-y-6">
              <!-- Subject Name -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Subject Name
                </label>
                <input
                  v-model="subjectData.name"
                  type="text"
                  required
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <!-- Description -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Description
                </label>
                <textarea
                  v-model="subjectData.description"
                  rows="3"
                  required
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                ></textarea>
              </div>

              <!-- Image Upload -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Subject Image
                </label>
                <input
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              <!-- Buttons -->
              <div class="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  @click="$emit('close')"
                  class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200"
                >
                  Create Subject
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slideUp-enter-active,
.slideUp-leave-active {
  transition: transform 0.3s ease;
}

.slideUp-enter-from,
.slideUp-leave-to {
  transform: translateY(100%);
}
</style>
