<!-- components/QuizInterface.vue -->
<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";

const router = useRouter();
const quizStore = useQuizStore();
const timeRemaining = ref(null);
let timerInterval;

const {
  quiz,
  currentQuestion,
  isLastQuestion,
  isFirstQuestion,
  questionProgress,
  userAnswers,
} = storeToRefs(quizStore);

const { setQuiz, setAnswer, nextQuestion, previousQuestion, submitQuiz } =
  quizStore;

// Initialize timer
const initializeTimer = () => {
  const startTime = parseInt(localStorage.getItem("quizStartTime"));
  const totalDuration = parseInt(localStorage.getItem("totalDuration"));

  if (!startTime) return;

  const updateTimer = () => {
    const now = new Date().getTime();
    const elapsed = Math.floor((now - startTime) / 1000);
    const remaining = totalDuration * 60 - elapsed;

    if (remaining <= 0) {
      clearInterval(timerInterval);
      handleSubmit();
    } else {
      timeRemaining.value = remaining;
    }
  };

  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
};

const formatTime = (seconds) => {
  if (!seconds) return "00:00";
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
    .toString()
    .padStart(2, "0")}`;
};

const selectOption = (questionId, optionId) => {
  setAnswer(questionId, optionId);
};

const getQuestionButtonClass = (index) => {
  if (index === currentQuestionIndex.value) {
    return "btn-primary";
  }
  return userAnswers.value.has(quiz.value.questions[index].id)
    ? "btn-success"
    : "btn-outline-secondary";
};

const handleSubmit = async () => {
  try {
    const answers = submitQuiz();
    // Call your API to submit the quiz
    // await axios.post(`/api/quizzes/${quiz.value.id}/submit`, { answers })

    // Clear localStorage
    localStorage.removeItem("quizStartTime");
    localStorage.removeItem("totalDuration");

    // Redirect to results page
    router.push("/quiz-results");
  } catch (error) {
    console.error("Error submitting quiz:", error);
  }
};

onMounted(() => {
  // Assuming you're passing the quiz data as a prop or fetching it
  // setQuiz(quizData)
  initializeTimer();
});

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});
</script>

<template>
  <div class="quiz-container">
    <!-- Timer and Progress -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <div class="progress" style="width: 70%">
            <div
              class="progress-bar"
              :style="{
                width: `${
                  (questionProgress.current / questionProgress.total) * 100
                }%`,
              }"
            >
              Question {{ questionProgress.current }} of
              {{ questionProgress.total }}
            </div>
          </div>
          <div class="timer" :class="{ 'text-danger': timeRemaining < 300 }">
            Time Remaining: {{ formatTime(timeRemaining) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Question Card -->
    <div class="card">
      <div class="card-body">
        <h4 class="card-title mb-4">{{ currentQuestion.title }}</h4>
        <p class="card-text">{{ currentQuestion.text }}</p>

        <!-- Options -->
        <div class="options-container">
          <div
            v-for="option in currentQuestion.options"
            :key="option.id"
            class="option mb-3"
          >
            <div
              class="option-card p-3"
              :class="{
                selected: userAnswers.get(currentQuestion.id) === option.id,
              }"
              @click="selectOption(currentQuestion.id, option.id)"
            >
              {{ option.text }}
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="d-flex justify-content-between mt-4">
          <button
            class="btn btn-secondary"
            @click="previousQuestion"
            :disabled="isFirstQuestion"
          >
            Previous
          </button>

          <div>
            <button
              v-if="!isLastQuestion"
              class="btn btn-primary"
              @click="nextQuestion"
            >
              Next
            </button>
            <button v-else class="btn btn-success" @click="handleSubmit">
              Submit Quiz
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Navigator -->
    <div class="card mt-4">
      <div class="card-body">
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="(_, index) in quiz.questions"
            :key="index"
            class="btn btn-sm"
            :class="getQuestionButtonClass(index)"
            @click="currentQuestionIndex = index"
          >
            {{ index + 1 }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.timer {
  font-size: 1.2rem;
  font-weight: bold;
}

.option-card {
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-card:hover {
  background-color: #f8f9fa;
  border-color: #0d6efd;
}

.option-card.selected {
  background-color: #0d6efd;
  color: white;
  border-color: #0d6efd;
}

.question-navigator {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
