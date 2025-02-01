<script setup>
import { ref, reactive, onMounted, useTemplateRef } from "vue";
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

const isLoading = ref(true);
const subjectName = ref(null);
const chapterName = ref(null);

const subjectId = route.params.subjectId;
const chapterId = route.params.chapterId;
const quizId = route.params.quizId;

const headerRef = useTemplateRef("headerRef");
const scrollToTop = () => {
  headerRef.value.scrollIntoView({ behavior: "smooth", block: "start" });
};

// Quiz data structure
const quizData = reactive({
  name: "",
  description: "",
  time_duration: "",
  deadline: "",
  price: 0,
  questions: [],
});

// Fetch all required data
const fetchData = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    // Fetch all data concurrently
    const [quizRes, subjectRes, chapterRes] = await Promise.all([
      axios.get(`${API_URL}/quizzes/${quizId}?include_answers=true`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get(`${API_URL}/subject/${subjectId}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get(`${API_URL}/chapter/${chapterId}`, {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);

    // Populate quiz data
    quizData.name = quizRes.data.name;
    quizData.description = quizRes.data.description;
    quizData.time_duration = quizRes.data.time_duration;
    quizData.price = quizRes.data.price;
    quizData.deadline = quizRes.data.deadline;
    quizData.questions = quizRes.data.questions.map((q) => ({
      id: q.id,
      title: q.title,
      text: q.text,
      options: q.options.map((opt) => ({
        id: opt.id,
        text: opt.text,
        is_correct: opt.is_correct,
      })),
    }));

    subjectName.value = subjectRes.data.name;
    chapterName.value = chapterRes.data.name;
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};

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
    quizData.questions[questionIndex].options.splice(optionIndex, 1);
  }
};

const removeQuestion = (index) => {
  if (quizData.questions.length > 1) {
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

    const correctOptionsCount = question.options.filter(
      (opt) => opt.is_correct
    ).length;

    if (correctOptionsCount === 0) {
      throw new Error(`Question ${idx + 1} must have one correct answer`);
    }

    if (correctOptionsCount > 1) {
      throw new Error(`Question ${idx + 1} can only have one correct answer`);
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

    const response = await axios.put(`${API_URL}/quizzes/${quizId}`, quizData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    console.log("Quiz updated:", response.data);

    router.push(
      `/admin/subject/${subjectId}/chapter/${chapterId}/quiz/${quizId}`
    );
  } catch (error) {
    alert(error.response?.data?.message || error.message);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <header
      ref="headerRef"
      class="h-16 bg-white flex sm:relative sticky top-0 items-center justify-between gap-6 mb-2"
    >
      <div class="flex items-center flex-1">
        <div class="flex-1 sm:max-w-lg">
          <h2 class="sm:text-3xl text-xl sm:ml-0 ml-12 font-bold sohne-mono">
            <span class="sm:text-[34px]">🡲</span> Edit Quiz
          </h2>
        </div>
      </div>

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

    <div class="py-4 sm:px-4 px-1 overflow-hidden">
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
        <RouterLink
          :to="`/admin/subject/${subjectId}/chapter/${chapterId}/quiz/${quizId}`"
          class="text-gray-500 hover:text-black sohne-mono"
        >
          {{ quizData.name }}
        </RouterLink>
        <span class="text-gray-500">/</span>
        <span class="text-black sohne-mono">Edit Quiz</span>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Quiz Details Section -->
        <div
          class="flex relative items-center justify-between bg-[#192227] text-[#fdfcfc] px-6 py-8 rounded-2xl shadow"
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

            <div class="sm:grid sm:grid-cols-2 flex flex-col gap-8 sm:gap-4">
              <div class="mt-2 flex flex-col gap-1">
                <label class="block sohne-mono font-medium"
                  >Time Duration［HH:MM］</label
                >
                <input
                  v-model="quizData.time_duration"
                  type="text"
                  required
                  placeholder="01:30"
                  pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
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

              <div class="mt-2 flex flex-col gap-1">
                <label class="block sohne-mono font-medium"
                  >Deadline (Optional)</label
                >
                <input
                  v-model="quizData.deadline"
                  type="datetime-local"
                  class="mt-1 block w-full border-b-2 bg-transparent border-[#fdfcfc] outline-none font-semibold"
                />
              </div>
            </div>
          </div>
          <div class="text-[200px] mt-[-40px] mb-[-40px] arrow">🡽</div>
        </div>

        <!-- Questions Section -->
        <div
          class="flex flex-col gap-4 bg-[#192227] text-[#fdfcfc] sm:p-6 py-8 px-4 rounded-3xl shadow overflow-hidden"
        >
          <div class="flex justify-between items-center">
            <h2 class="sm:text-2xl text-lg font-bold sohne-mono">
              Questions ［{{ quizData.questions.length }}］
            </h2>
            <button
              type="button"
              @click="addQuestion"
              class="sm:px-4 px-2 py-2 bg-[#f9e000] text-[#192227] rounded-lg hover:scale-95 transition-all duration-200 ease-linear sohne-mono sm:text-base text-sm font-bold flex items-center gap-2"
            >
              <component
                :is="AddIcon"
                class="sm:w-6 sm:h-6 w-4 h-4 fill-[#192227]"
              />
              New Question
            </button>
          </div>

          <!-- Individual Questions -->
          <div
            v-for="(question, qIndex) in quizData.questions"
            :key="qIndex"
            class="bg-[#192227] sm:p-6 rounded-lg shadow sm:space-y-12 space-y-8"
          >
            <div class="flex justify-between items-start">
              <h3 class="font-medium text-lg">Question {{ qIndex + 1 }}.</h3>
              <button
                type="button"
                @click="removeQuestion(qIndex)"
                class="px-2 py-2 sm:text-base text-xs flex items-center gap-2 text-[#f9e000] bg-[#192227] rounded-lg transition-all hover:scale-95 duration-200 sohne-mono font-bold"
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
                  Options ［{{ question.options.length }}］
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

        <!-- Action Buttons -->
        <div class="flex sm:justify-end justify-between gap-4">
          <button
            type="button"
            @click="scrollToTop"
            class="sm:px-6 px-3 text-sm sm:text-base py-2 border-2 border-[#192227] text-[#192227] rounded-lg hover:bg-gray-100 sohne-mono"
          >
            Back to Top
          </button>
          <button
            type="button"
            @click="router.back()"
            class="sm:px-6 py-2 px-3 text-sm sm:text-base border-2 border-[#192227] text-[#192227] rounded-lg hover:bg-gray-100 sohne-mono"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="sm:px-6 py-2 px-3 text-sm sm:text-base bg-[#192227] text-white rounded-lg hover:bg-gray-800 sohne-mono"
          >
            Save Changes
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

@media (max-width: 768px) {
  .arrow {
    position: absolute;
    opacity: 0.2;
    right: 0;
    scale: 3;
  }

  input {
    font-size: 18px;
  }
}
</style>
