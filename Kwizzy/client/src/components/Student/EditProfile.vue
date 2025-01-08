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
    <div v-if="isOpen" class="fixed inset-0 z-50" @click="$emit('close')">
      <div
        class="flex items-center justify-center relative min-h-screen"
        @click.stop
      >
        <div
          ref="modalRef"
          class="bg-[#fff9f0] text-orange-600 rounded-3xl sm:w-[700px] w-[400px]"
        >
          <!-- Header -->
          <div class="sm:px-6 px-4 pt-4 pb-2">
            <h3 class="text-3xl tracking-tighter font-bold">Edit Profile</h3>
          </div>
          <button
            @click="$emit('close')"
            class="absolute top-4 right-4 bg-[#f0f0f0] p-1 text-black hover:bg-[#f0f0ff] rounded-md transition-colors duration-200 ease-linear flex items-center gap-1"
          >
            <component :is="CloseIcon" class="w-6 h-6" />[<span
              class="sohne-mono"
              >ESC</span
            >]
          </button>

          <!-- Content -->
          <div class="sm:px-6 px-4 py-2">
            <form @submit.prevent="handleSubmit">
              <div class="mb-4">
                <label for="name" class="text-sm font-semibold">Name</label>
                <input
                  v-model="studentData.name"
                  type="text"
                  id="name"
                  class="w-full bg-[#fff9f0] border-b-2 border-orange-600 focus:outline-none"
                />
              </div>

              <div class="mb-4">
                <label for="email" class="text-sm font-semibold">Email</label>
                <input
                  v-model="studentData.email"
                  type="email"
                  id="email"
                  class="w-full bg-[#fff9f0] border-b-2 border-orange-600 focus:outline-none"
                />
              </div>

              <div class="mb-4">
                <label for="qualification" class="text-sm font-semibold"
                  >Qualification</label
                >
                <input
                  v-model="studentData.qualification"
                  type="text"
                  id="qualification"
                  class="w-full bg-[#fff9f0] border-b-2 border-orange-600 focus:outline-none"
                />
              </div>

              <div class="mb-4">
                <input
                  type="file"
                  @change="handleImageUpload"
                  id="profile_pic"
                  accept="image/*"
                  class="hidden"
                  ref="fileInput"
                />
                <div
                  class="relative w-40 h-40 border-2 border-dashed border-orange-600 rounded-lg cursor-pointer hover:bg-[#fff9f0]"
                  @click="triggerFileInput"
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
              </div>
              <!-- Actions -->
              <div
                class="sm:px-6 px-4 py-4 pt-0 bg-[#fff9f0] rounded-3xl flex justify-end gap-2"
              >
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
            </form>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { useToast } from "@/composables/useToast";
const toast = useToast();
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
const emit = defineEmits(["close", "update"]);
const modalRef = ref(null);
const preview = ref(null);
const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

import CloseIcon from "../../assets/images/icons/close.svg";

const props = defineProps({
  isOpen: Boolean,
  student: {
    type: Object,
    required: true,
  },
});

const studentData = ref({
  name: "",
  email: "",
  qualification: "",
  profile_pic: null,
});

const initializeForm = (student) => {
  studentData.value = {
    name: student.name,
    email: student.email,
    qualification: student.qualification,
    image: null,
  };

  console.log("student ", student);

  if (student.profile_pic) {
    preview.value = `${student.profile_pic}`;
  } else {
    preview.value = null;
  }
};

const handleEscKey = (event) => {
  if (event.key === "Escape" && props.isOpen) {
    emit("close");
  }
};

watch(
  () => props.student,
  (newStudent) => {
    if (newStudent) {
      initializeForm(newStudent);
    }
  },
  { immediate: true }
);

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    studentData.value.image = file; // Fixed variable name
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

const handleSubmit = async () => {
  const formData = new FormData();
  formData.append("name", studentData.value.name);
  formData.append("email", studentData.value.email);
  formData.append("qualification", studentData.value.qualification);
  // Only append image if a new one was selected
  if (studentData.value.image instanceof File) {
    formData.append("profile_pic", studentData.value.image);
  }

  formData.append("keep_existing_image", preview.value ? "true" : "false");

  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("No access token available");
    }

    const studentId = props.student.student_info?.id || props.student.id;

    const response = await axios.put(`${API_URL}/user/${studentId}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
      },
    });

    emit("update", response.data);
    toast.success(response.data.message);
    emit("close");
  } catch (error) {
    console.error("Server response data:", error);
    alert(error.response?.data?.message || "Error during update");
  }
};

onMounted(() => {
  document.addEventListener("keydown", handleEscKey);
});

onUnmounted(() => {
  if (preview.value && preview.value.startsWith("blob:")) {
    URL.revokeObjectURL(preview.value);
  }
  document.removeEventListener("keydown", handleEscKey);
});
</script>

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
