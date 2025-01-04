<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Sidebar from "@/components/Admin/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import logo from "@/assets/images/landing-page/white logo.png";
import AddIcon from "@/assets/images/icons/add.svg";
import DeleteIcon from "@/assets/images/icons/delete.svg";

const route = useRoute();
const router = useRouter();

const API_URL = import.meta.env.VITE_API_URL;

const subjectName = ref(null);
const chapterName = ref(null);

const isLoading = ref(false);
const chapterId = route.params.chapterId;
const subjectId = route.params.subjectId;

const getNames = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");
    const [subjectRes, chapterRes] = await Promise.all([
      axios.get(`${API_URL}/subject/${subjectId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
      axios.get(`${API_URL}/chapter/${chapterId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
    ]);
    subjectName.value = subjectRes.data.name;
    chapterName.value = chapterRes.data.name;
  } catch (error) {
    console.log("Error", error);
  } finally {
    isLoading.value = false;
  }
};

// Initialize with one question
const quizData = reactive({
  name: "",
  description: "",
  time_duration: "",
  price: 0,
  questions: [
    {
      title: "",
      text: "",
      options: [
        { text: "", is_correct: false },
        { text: "", is_correct: false },
        { text: "", is_correct: false },
        { text: "", is_correct: false },
      ],
    },
  ],
});

// Add a new question
const addQuestion = () => {
  quizData.questions.push({
    title: "",
    text: "",
    options: [
      { text: "", is_correct: false },
      { text: "", is_correct: false },
      { text: "", is_correct: false },
      { text: "", is_correct: false },
    ],
  });
};

// Add option to a specific question
const addOption = (questionIndex) => {
  quizData.questions[questionIndex].options.push({
    text: "",
    is_correct: false,
  });
};

// Remove option from a specific question
const removeOption = (questionIndex, optionIndex) => {
  if (quizData.questions[questionIndex].options.length > 2) {
    // Minimum 2 options
    quizData.questions[questionIndex].options.splice(optionIndex, 1);
  }
};

const removeQuestion = (index) => {
  if (quizData.questions.length > 1) {
    // Keep at least one question
    quizData.questions.splice(index, 1);
  }
};

// Validation function
const validateQuiz = () => {
  if (!quizData.name || !quizData.description || !quizData.time_duration) {
    throw new Error("Please fill in all required quiz details");
  }

  if (quizData.questions.length === 0) {
    throw new Error("Quiz must have at least one question");
  }

  quizData.questions.forEach((question, idx) => {
    if (!question.text) {
      throw new Error(`Question ${idx + 1} text is required`);
    }

    if (question.options.length < 2) {
      throw new Error(`Question ${idx + 1} must have at least 2 options`);
    }

    const hasCorrectOption = question.options.some((opt) => opt.is_correct);
    if (!hasCorrectOption) {
      throw new Error(
        `Question ${idx + 1} must have at least one correct answer`
      );
    }

    const hasEmptyOption = question.options.some((opt) => !opt.text.trim());
    if (hasEmptyOption) {
      throw new Error(`All options in Question ${idx + 1} must have text`);
    }
  });
};

const handleSubmit = async () => {
  try {
    isLoading.value = true;
    validateQuiz();

    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.post(
      `${API_URL}/quizzes`,
      {
        ...quizData,
        chapter_id: chapterId,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    router.push(
      `/admin/subject/${route.params.subjectId}/chapter/${chapterId}`
    );
  } catch (error) {
    alert(error.response?.data?.message || error.message);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  getNames();
});
</script>

<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <header class="h-16 bg-white flex items-center justify-between gap-6 mb-2">
      <div class="flex items-center flex-1">
        <div class="flex-1 max-w-lg">
          <h2 class="text-3xl font-bold sohne-mono">
            <span class="text-[34px]">🡲</span> Quiz Form
          </h2>
        </div>
      </div>

      <!-- Right Side Icons -->
      <div class="flex items-center">
        <div class="flex items-center gap-4">
          <img
            :src="logo"
            alt="User avatar"
            class="w-8 h-8 rounded-full mix-blend-difference"
          />
          <span class="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </header>
    <div class="py-4 px-4">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-2 text-sm mb-6">
        <RouterLink
          to="/admin"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          Subjects
        </RouterLink>
        <span class="text-gray-500">/</span>
        <RouterLink
          :to="`/admin/subject/${subjectId}`"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          {{ subjectName }}
        </RouterLink>
        <span class="text-gray-500">/</span>
        <RouterLink
          :to="`/admin/subject/${subjectId}/chapter/${chapterId}`"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          {{ chapterName }}
        </RouterLink>
        <span class="text-gray-500">/</span>
        <span class="text-gray-500 sohne-mono">Create Quiz</span>
      </div>
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Quiz Details Section -->
        <div
          class="flex items-center justify-between bg-[#192227] text-[#fdfcfc] px-6 py-4 rounded-2xl shadow"
        >
          <div class="flex-1 flex flex-col gap-12">
            <div>
              <label class="block sohne-mono font-medium">Quiz Name *</label>
              <input
                v-model="quizData.name"
                type="text"
                required
                class="mt-1 block w-full bg-transparent font-[Inter] font-semibold outline-none border-b-2 border-[#fdfcfc]"
              />
            </div>

            <div>
              <label class="block sohne-mono font-medium">Description *</label>
              <textarea
                v-model="quizData.description"
                rows="1"
                required
                class="mt-1 py-1 block w-full bg-transparent border-[#fdfcfc] shadow-sm border-b-2 outline-none"
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="mt-2 flex flex-col gap-1">
                <label class="block sohne-mono font-medium"
                  >Time Duration (hh:mm) *</label
                >
                <input
                  v-model="quizData.time_duration"
                  type="text"
                  required
                  class="mt-1 block w-full border-b-2 bg-transparent border-[#fdfcfc] outline-none font-semibold"
                />
              </div>

              <div class="mt-2 flex flex-col gap-1">
                <label class="block sohne-mono font-medium"
                  >Price (₹0 for free)</label
                >
                <input
                  v-model="quizData.price"
                  type="number"
                  min="0"
                  class="mt-1 block w-full border-b-2 border-[#fdfcfc] outline-none bg-transparent font-semibold"
                />
              </div>
            </div>
          </div>
          <div class="text-[300px] mt-[-40px] mb-[-60px]">🡽</div>
        </div>

        <!-- Questions Section -->
        <div
          class="space-y-6 bg-[#192227] text-[#fdfcfc] p-6 rounded-3xl shadow"
        >
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold sohne-mono">
              Questions
              <span class="font-mono text-[26px]"
                >[{{ quizData.questions.length }}]</span
              >
            </h2>
            <button
              type="button"
              @click="addQuestion"
              class="px-4 py-2 bg-[#f9e000] text-[#192227] rounded-lg hover:scale-95 transition-all duration-200 ease-linear sohne-mono font-bold flex items-center gap-2"
            >
              <component :is="AddIcon" class="w-6 h-6 fill-[#192227]" />
              New Question
            </button>
          </div>

          <!-- Individual Questions -->
          <div
            v-for="(question, qIndex) in quizData.questions"
            :key="qIndex"
            class="bg-[#192227] p-6 rounded-lg shadow space-y-4"
          >
            <div class="flex justify-between items-start">
              <h3 class="font-medium text-lg">Question {{ qIndex + 1 }}.</h3>
              <button
                type="button"
                @click="removeQuestion(qIndex)"
                class="px-2 py-2 flex items-center gap-2 text-[#f9e000] bg-[#192227] rounded-lg transition-all hover:scale-95 duration-200 sohne-mono font-bold"
                :disabled="quizData.questions.length === 1"
              >
                <component
                  :is="DeleteIcon"
                  class="w-4 h-4 fill-[#f9e000] hover:fill-[#de0000] transition-all duration-300 ease"
                />
                Delete Question
              </button>
            </div>

            <div>
              <label class="block text-sm font-medium sohne-mono"
                >Question Title (Optional)</label
              >
              <input
                v-model="question.title"
                type="text"
                class="mt-1 block w-full border-b-2 bg-transparent border-[#fdfcfc] outline-none font-semibold"
              />
            </div>

            <div>
              <label class="block text-sm font-medium sohne-mono"
                >Question Text *</label
              >
              <textarea
                v-model="question.text"
                required
                rows="1"
                class="mt-2 block w-full bg-transparent border-[#fdfcfc] shadow-sm border-b-2 outline-none"
              ></textarea>
            </div>

            <!-- Options -->
            <div class="flex flex-col gap-4 pt-8">
              <div class="flex justify-between items-center">
                <h4 class="font-medium sohne-mono">
                  Options
                  <span class="tracking-tighter"
                    >[{{ question.options.length }}]</span
                  >
                </h4>
                <button
                  type="button"
                  @click="addOption(qIndex)"
                  class="text-[#fdfcfc] text-sm sohne-mono hover:scale-95 transition-all duration-200"
                >
                  + Add Option
                </button>
              </div>

              <div
                v-for="(option, oIndex) in question.options"
                :key="oIndex"
                class="flex items-center gap-3 group"
              >
                <div class="flex-shrink-0">
                  <input
                    v-model="option.is_correct"
                    type="checkbox"
                    class="w-4 h-4"
                  />
                </div>

                <input
                  v-model="option.text"
                  type="text"
                  required
                  :placeholder="`${oIndex + 1}`"
                  class="flex-1 bg-transparent border-b-2 border-[#fdfcfc] outline-none option-input font-semibold"
                />

                <button
                  type="button"
                  @click="removeOption(qIndex, oIndex)"
                  class="opacity-0 group-hover:opacity-100 text-[#f9e000] sohne-mono px-2 py-1 transition-all hover:scale-95 duration-200 text-sm"
                  :disabled="question.options.length <= 2"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-end gap-4">
          <button
            type="button"
            @click="router.back()"
            class="px-6 py-2 border-2 border-black text-black rounded-lg hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            {{ isLoading ? "Creating Quiz..." : "Create Quiz" }}
          </button>
        </div>
      </form>
    </div>
  </Sidebar>
</template>

<style scoped>
.shadow {
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}
input {
  font-size: 24px;
}

label {
  font-size: 14px;
}

.option-input {
  font-size: 16px;
}

.option-input::placeholder {
  font-size: 16px;
}
</style>
