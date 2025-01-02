<!-- components/CreateSubjectModal.vue -->
<script setup>
import { ref } from "vue";
const props = defineProps({ isOpen: Boolean });
const emit = defineEmits(["close", "create"]);
const modalRef = ref(null);
const subjectData = ref({ name: "", description: "", image: null });
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
  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <!-- Backdrop with its own transition -->
      <Transition name="backdrop">
        <div
          class="absolute inset-0 bg-black/20 backdrop-blur-sm"
          @click="$emit('close')"
        ></div>
      </Transition>

      <!-- Modal with its own transition -->
      <Transition name="modal-content">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div
            ref="modalRef"
            class="bg-white rounded-2xl w-full max-w-[500px] p-6 relative z-10"
            @click.stop
          >
            <!-- Your existing modal content -->
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
              Create New Subject
            </h2>

            <form @submit.prevent="handleSubmit" class="space-y-6">
              <!-- Your existing form content -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Subject Name
                </label>
                <input
                  v-model="subjectData.name"
                  type="text"
                  required
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-black focus:border-transparent outline-none"
                />
              </div>

              <!-- Description -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  v-model="subjectData.description"
                  rows="3"
                  required
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-black focus:border-transparent outline-none"
                ></textarea>
              </div>

              <!-- Image Upload -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Subject Image
                </label>
                <input
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-900"
                />
              </div>

              <!-- Buttons -->
              <div class="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  @click="$emit('close')"
                  class="px-4 py-2 rounded-lg border-2 border-black text-black hover:bg-black hover:text-white transition-colors duration-200 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 rounded-lg bg-black text-white hover:bg-white hover:text-black border-2 border-black font-semibold transition-colors duration-200"
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
/* Backdrop transitions */
.backdrop-enter-active,
.backdrop-leave-active {
  transition: all 0.3s ease-out;
}

.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
  backdrop-filter: blur(0);
}

.backdrop-enter-to,
.backdrop-leave-from {
  opacity: 1;
  backdrop-filter: blur(4px);
}

/* Modal content transitions */
.modal-content-enter-active,
.modal-content-leave-active {
  transition: all 0.3s ease-out;
}

.modal-content-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.modal-content-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

/* Overall modal container transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Optional: Add smooth transitions to form elements */
input,
textarea,
button {
  transition: all 0.2s ease;
}

input:focus,
textarea:focus {
  transform: translateY(-1px);
}

button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>
