<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import CloseIcon from "../../assets/images/icons/close.svg";

const props = defineProps({
  isOpen: Boolean,
  subjectId: {
    type: [String, Number],
    required: true,
  },
  subjectName: {
    type: String,
    required: true,
  },
  chapter: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["close", "create"]);
const chapterData = ref({
  name: "",
  description: "",
  subject_id: props.subjectId,
});

const old_chapter_name = props.chapter.name;

onMounted(() => {
  if (props.chapter) {
    chapterData.value = {
      name: props.chapter.name,
      description: props.chapter.description,
      subject_id: props.chapter.subject_id,
    };
  }
});

const handleSubmit = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.put(
      `${API_URL}/chapter/${props.chapter.id}`,
      chapterData.value,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    console.log("Response:", response.data.chapter);
    emit("update", response.data.chapter);
    emit("close");
  } catch (error) {
    console.error("Error updating chapter:", error);
    alert(error.response?.data?.message || "Error updating chapter");
  }
};
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen">
      <div
        class="absolute inset-0 bg-black/20 backdrop-blur-[3px]"
        @click="$emit('close')"
      ></div></div
  ></Transition>

  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <div class="flex items-center justify-center min-h-screen pb-24">
        <div
          ref="modalRef"
          class="bg-white shadow-2xl rounded-xl w-full max-w-[700px] p-3 px-4 relative z-10"
          @click.stop
        >
          <div class="flex justify-between items-center mb-4">
            <p class="sohne-mono">
              <span class="text-gray-500">{{ subjectName }} / </span
              ><span class="text-gray-500">{{ old_chapter_name }}</span> / Edit
              Chapter
            </p>
            <button
              @click="$emit('close')"
              class="p-1 text-gray-700 hover:bg-[#f0f0ff] rounded-md transition-colors duration-200 ease-linear"
            >
              <component :is="CloseIcon" class="w-6 h-6" />
            </button>
          </div>

          <form @submit.prevent="handleSubmit">
            <div>
              <input
                v-model="chapterData.name"
                type="text"
                required
                class="w-full bg-white font-semibold text-gray-800 outline-none subject-input mb-3"
                placeholder="Chapter Name"
              />
            </div>

            <!-- Description -->
            <div>
              <textarea
                v-model="chapterData.description"
                rows="3"
                required
                class="w-full bg-white text-gray-900 description resize-none outline-none"
                placeholder="Add description..."
                >{{ chapterData.description }}</textarea
              >
            </div>

            <div>
              <input type="text" v-model="chapterData.subject_id" hidden />
            </div>
            <hr />
            <!-- Buttons -->
            <div class="flex justify-end gap-3 mt-3">
              <button
                type="button"
                @click="$emit('close')"
                class="px-4 py-2 rounded-lg text-[14px] border-2 border-black text-black transition-colors duration-200 font-semibold button"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1 rounded-lg text-[14px] bg-black text-white border-2 border-black font-semibold transition-colors duration-200 button"
              >
                Save Changes
              </button>
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
