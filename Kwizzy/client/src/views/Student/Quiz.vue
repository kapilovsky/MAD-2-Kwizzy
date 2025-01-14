<template>
  <div class="container mx-auto sm:px-4 py-8">
    <div
      v-if="isLoading || isCheckingPayment"
      class="flex justify-center items-center h-64"
    >
      <Loader />
    </div>

    <div v-else-if="quiz">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-2 text-gray-600 text-sm mb-4">
        <RouterLink
          :to="{
            name: 'student-dashboard',
            params: {
              id: studentId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >Dashboard</RouterLink
        >
        <span>/</span>
        <RouterLink
          :to="{
            name: 'view-subjects',
            params: {
              id: studentId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >Subjects</RouterLink
        >
        <span>/</span>
        <RouterLink
          :to="{
            name: 'subject',
            params: {
              id: studentId,
              subjectId: subjectId,
            },
          }"
          class="text-gray-500 hover:text-black sohne-mono"
          >{{ subjectName }}</RouterLink
        >

        <span>/</span>
        <RouterLink
          :to="{
            name: 'chapter',
            params: {
              id: studentId,
              subjectId: subjectId,
              chapterId: chapterId,
            },
          }"
          class="text-black sohne-mono"
          >{{ chapterName }}</RouterLink
        >
      </div>

      <div class="bg-[#192227] text-[#fdfcfc] p-6 rounded-2xl shadow">
        <div class="flex justify-between">
          <div class="space-y-4">
            <div>
              <h1 class="text-3xl font-bold">{{ quiz?.name }}</h1>
              <p class="text-gray-300 mt-2">{{ quiz?.description }}</p>
            </div>
            <div class="flex gap-8">
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Duration</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.time_duration }}
                </p>
              </div>
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Price</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.price ? `₹${quiz.price}` : "Free" }}
                </p>
              </div>
              <div>
                <span class="text-gray-400 sohne-mono text-sm">Questions</span>
                <p class="text-xl font-semibold">
                  {{ quiz?.questions?.length || 0 }}
                </p>
              </div>
            </div>
          </div>
          <div
            class="text-[760px] absolute sm:-bottom-[300px] bottom-20 -right-10 sm:right-0 opacity-20 z-1 select-none"
            style="pointer-events: none"
          >
            🡽
          </div>
        </div>

        <div>
          <h3 class="sohne-mono text-lg mb-2 mt-8">Instructions</h3>
          <ul class="sohne">
            <li>🡪 You cannot pause the quiz once started</li>
            <li>🡪 Timer will continue even if you close the browser</li>
            <li>🡪 Each question has only one correct answer</li>
            <li>🡪 You can review your answers before final submission</li>
          </ul>
        </div>

        <button
          v-if="quiz?.price > 0 && !hasPaid"
          @click="showPaymentModal"
          class="w-full bg-[#fdfcfc] py-3 rounded-lg transition-colors disabled:bg-gray-400 mt-8 sm:text-right relative group overflow-hidden"
          :disabled="isProcessing"
        >
          <span
            class="arame sm:text-5xl text-2xl sm:mr-20 cursor-pointer text-[#192227]"
          >
            Pay ₹{{ quiz.price }}
          </span>
          <span
            class="absolute sm:text-5xl text-2xl right-7 top-1/2 transform -translate-y-1/2 text-[#192227] opacity-0 group-hover:opacity-100 group-hover:translate-x-2 transition-all"
          >
            🡲
          </span>
        </button>

        <button
          v-else
          @click="showStartDialog"
          class="w-full bg-[#fdfcfc] py-3 rounded-lg transition-colors disabled:bg-gray-400 mt-8 sm:text-right relative group overflow-hidden"
          :disabled="isStarting"
        >
          <span
            class="arame sm:text-5xl text-2xl sm:mr-20 cursor-pointer text-[#192227]"
            >Start Quiz</span
          ><span
            class="absolute sm:text-5xl text-2xl right-7 top-1/2 transform -translate-y-1/2 text-[#192227] opacity-0 group-hover:opacity-100 group-hover:translate-x-2 transition-all"
          >
            🡲
          </span>
        </button>

        <MockPaymentModal
          v-if="showPayment"
          :amount="quiz?.price"
          @close="showPayment = false"
          @success="handlePaymentSuccess"
        />
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <!-- Start Quiz Dialog -->
    <transition name="fade" mode="out-in">
      <DialogModal
        v-if="isDialogOpen"
        @close="isDialogOpen = false"
        @confirm="startQuiz"
      >
        <template #title>Start Quiz</template>
        <template #content>
          <p class="font-mono font-semibold tracking-tighter text-lg">
            Are you ready to start the quiz? Once started:
          </p>
          <ul
            class="list-disc list-inside font-medium tracking-[-0.5px] text-sm sm:text-base"
          >
            <li>The timer will begin immediately.</li>
            <li>You cannot pause or restart.</li>
            <li>Make sure you have a stable internet connection.</li>
          </ul>
        </template>
        <template #actions>
          <button
            class="px-4 py-2 text-orange-600 font-bold"
            @click="isDialogOpen = false"
          >
            Cancel
          </button>
          <button
            @click="startQuiz"
            class="px-4 py-2 bg-orange-200 text-orange-600 rounded-xl hover:bg-[#ffe4bb] hover:text-orange-700 transition-all duration-300 font-bold"
          >
            Start Now
          </button>
        </template>
      </DialogModal>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { storeToRefs } from "pinia";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useToast } from "@/composables/useToast";
import DialogModal from "@/components/DialogModal.vue";
import Loader from "@/components/Loader.vue";
import MockPaymentModal from "@/components/Student/MockPaymentModal.vue";
import { BreadcrumbsStore } from "@/stores/breadcrumbsStore";
const breadcrumbStore = BreadcrumbsStore();
const { subjectName, chapterName } = storeToRefs(breadcrumbStore);
const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const route = useRoute();
const toast = useToast();

const quiz = ref(null);
const hasPaid = ref(false);
const error = ref(null);
const isLoading = ref(true);
const isStarting = ref(false);
const isDialogOpen = ref(false);
const showPayment = ref(false);
const isProcessing = ref(false);
const isCheckingPayment = ref(true);
const studentId = route.params.id;
const subjectId = route.params.subjectId;
const chapterId = route.params.chapterId;

const showPaymentModal = () => {
  showPayment.value = true;
};

const handlePaymentSuccess = async (paymentDetails) => {
  try {
    isProcessing.value = true;
    const token = localStorage.getItem("access_token");

    await axios.post(
      `${API_URL}/payments`,
      {
        quiz_id: route.params.quizId,
        transaction_id: paymentDetails.transactionId,
        amount: paymentDetails.amount,
        user_id: studentId,
      },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    showPayment.value = false;
    hasPaid.value = true;
    toast.success("Payment successful!");
    showStartDialog();
  } catch (error) {
    console.error("Error processing payment:", error);
    toast.error("Failed to process payment");
  } finally {
    isProcessing.value = false;
  }
};

const checkPaymentStatus = async () => {
  try {
    isCheckingPayment.value = true;
    const token = localStorage.getItem("access_token");
    const response = await axios.get(
      `${API_URL}/payments/status/${studentId}/${route.params.quizId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    hasPaid.value = response.data.has_paid;
  } catch (error) {
    console.error("Error checking payment status:", error);
  } finally {
    isCheckingPayment.value = false;
  }
};

const fetchQuizDetails = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token available");

    const response = await axios.get(
      `${API_URL}/quizzes/${route.params.quizId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    quiz.value = response.data;
  } catch (err) {
    console.error("Error fetching quiz:", err);
    error.value = "Failed to load quiz details";
    toast.error("Error loading quiz details");
  } finally {
    isLoading.value = false;
  }
};

const fetchBreadcrumbsIfNeeded = async () => {
  if (!subjectName.value || !chapterName.value) {
    try {
      isLoading.value = true;
      const token = localStorage.getItem("access_token");
      const [subjectRes, chapterRes] = await Promise.all([
        axios.get(`${API_URL}/subject/${subjectId}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${API_URL}/chapter/${chapterId}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      breadcrumbStore.setBreadcrumbs({
        subjectName: subjectRes.data.name,
        chapterName: chapterRes.data.name,
        subjectId: subjectId,
        chapterId: chapterId,
      });
    } catch (error) {
      console.error("Error fetching breadcrumb data:", error);
    } finally {
      isLoading.value = false;
    }
  }
};

const showStartDialog = () => {
  isDialogOpen.value = true;
};

const startQuiz = async () => {
  try {
    isStarting.value = true;
    isDialogOpen.value = false;

    router.push(`${route.path}/take`);
  } catch (err) {
    console.error("Error starting quiz:", err);
    toast.error("Failed to start quiz");
    isStarting.value = false;
  }
};

onMounted(async () => {
  await Promise.all([
    fetchQuizDetails(),
    fetchBreadcrumbsIfNeeded(),
    checkPaymentStatus(),
  ]);
});

onUnmounted(() => {
  breadcrumbStore.clearBreadcrumbs();
});
</script>

<style scoped>
.arame {
  font-family: arame;
}
</style>
