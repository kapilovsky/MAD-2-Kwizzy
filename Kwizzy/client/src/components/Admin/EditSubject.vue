<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
const props = defineProps({
  isOpen: Boolean,
  subject: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["close", "update"]);
const modalRef = ref(null);
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
const subjectData = ref({ name: "", description: "", image: null });
const preview = ref(null);
import CloseIcon from "../../assets/images/icons/close.svg";

// Initialize form with existing subject data
const initializeForm = (subject) => {
  subjectData.value = {
    name: subject.name,
    description: subject.description,
    image: null, // Don't set the image directly, just handle the preview
  };

  if (subject.subject_image) {
    preview.value = `${API_URL}/uploads/subjects/${subject.subject_image}`;
  } else {
    preview.value = null;
  }
};

const handleEscKey = (event) => {
  if (event.key === "Escape" && props.isOpen) {
    emit("close");
  }
};

// Watch for changes in the subject prop
watch(
  () => props.subject,
  (newSubject) => {
    if (newSubject) {
      initializeForm(newSubject);
    }
  },
  { immediate: true }
);

const handleSubmit = async (subject) => {
  const formData = new FormData();
  formData.append("name", subjectData.value.name);
  formData.append("description", subjectData.value.description);
  // Only append image if a new one was selected
  if (subjectData.value.image instanceof File) {
    formData.append("image", subjectData.value.image);
  }

  // Add a flag to indicate if the image should be kept or removed
  formData.append("keep_existing_image", preview.value ? "true" : "false");

  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }

    const response = await axios.put(
      `${API_URL}/subject/${props.subject.id}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    emit("update", response.data);
    console.log("Response:", response.data);
    emit("close");
  } catch (error) {
    console.error("Server response data:", error.response?.data);
    alert(error.response?.data?.message || "Error during update");
  }
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    subjectData.value.image = file;
    preview.value = URL.createObjectURL(file);
  }
};

const removeImage = (event) => {
  event.preventDefault();
  preview.value = null;
  subjectData.value.image = null;
  const fileInput = event.target
    .closest("label")
    .querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.value = "";
  }
};

onMounted(() => {
  window.addEventListener("keydown", handleEscKey);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleEscKey);
});
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen">
      <div
        class="absolute inset-0 bg-black/20 backdrop-blur-[3px]"
        @click="$emit('close')"
      ></div>
    </div>
  </Transition>

  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <div class="flex items-center justify-center min-h-screen pb-24">
        <div
          ref="modalRef"
          class="bg-white shadow-2xl rounded-xl w-full max-w-[750px] p-3 px-4 relative z-10"
          @click.stop
        >
          <div class="relative">
            <p class="sohne-mono mb-4">
              <span class="text-gray-500">{{ subject.name }}</span> / Edit
              Subject
            </p>
            <button
              @click="$emit('close')"
              class="absolute top-0 right-0 bg-[#f0f0f0] p-1 text-black hover:bg-[#f0f0ff] rounded-md transition-colors duration-200 ease-linear flex items-center gap-1"
            >
              <component :is="CloseIcon" class="w-6 h-6" />[<span
                class="sohne-mono"
                >ESC</span
              >]
            </button>
          </div>
          <form @submit.prevent="handleSubmit(subject)">
            <div>
              <input
                v-model="subjectData.name"
                type="text"
                required
                class="w-full bg-white font-semibold text-gray-800 outline-none subject-input mb-3"
                placeholder="Subject Name"
              />
            </div>

            <div>
              <textarea
                v-model="subjectData.description"
                rows="3"
                required
                class="w-full bg-white text-gray-900 description resize-none outline-none"
                placeholder="Add description..."
              ></textarea>
            </div>

            <div class="flex items-end justify-between">
              <label class="block">
                <input
                  type="file"
                  @change="handleImageUpload"
                  accept="image/*"
                  class="hidden"
                />
                <div
                  class="relative w-40 h-40 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50"
                >
                  <button
                    type="button"
                    v-if="preview"
                    @click.stop="removeImage"
                    class="absolute -top-2 -right-2 bg-black text-white rounded-full p-1 hover:bg-red-600 shadow-md z-10"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="3"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                  <img
                    v-if="preview"
                    :src="preview"
                    class="w-full h-full object-cover rounded-lg"
                  />
                  <div
                    v-else
                    class="absolute inset-0 flex flex-col items-center justify-center"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-10 w-10 text-[#acacac]"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <span class="mt-2 text-sm font-medium text-[#acacac]"
                      >Choose Image</span
                    >
                  </div>
                </div>
              </label>

              <div class="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  @click="$emit('close')"
                  class="px-4 py-1 rounded-lg text-[12px] border-2 border-black text-black transition-colors duration-200 font-semibold button"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="px-4 py-1 rounded-lg text-[12px] bg-black text-white border-2 border-black font-semibold transition-colors duration-200 button"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.sohne-mono {
  font-family: sohne-mono;
  text-transform: uppercase;
}
/* Overall modal container transition */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s ease-in-out;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateZ(100px);
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.subject-input {
  font-size: 18px;
  font-weight: 700;
  font-family: Inter;
  letter-spacing: -0.5px;
}
.subject-input::placeholder {
  color: #acacac;
  font-weight: 700;
  font-family: Inter;
  letter-spacing: -0.5px;
  font-size: 18px;
}

.description::placeholder {
  color: #acacac;
  font-weight: 500;
  font-family: Inter;
  letter-spacing: -0.5px;
  font-size: 15px;
}

textarea {
  resize: none;
  font-size: 15px;
  font-weight: 500;
  font-family: Inter;
  letter-spacing: -0.5px;
  font-size: 15px;
}

textarea::-webkit-scrollbar {
  width: 12px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
}

textarea::-webkit-scrollbar-thumb {
  background: #888;
}

.button {
  transition: all 0.2s ease-in-out;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 6px rgba(0, 0, 0, 0.1);
}

.button:active {
  transform: translateY(0);
}
</style>
