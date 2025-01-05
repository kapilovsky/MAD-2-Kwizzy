<!-- components/Toast/ToastContainer.vue -->
<script setup>
import { useToastStore } from "@/stores/toastStore";
import { storeToRefs } from "pinia";
import CheckCircleIcon from "../assets/images/icons/check-circle.svg";
import XCircleIcon from "../assets/images/icons/x-circle.svg";
import ExclamationCircleIcon from "../assets/images/icons/warning.svg";
import InformationCircleIcon from "../assets/images/icons/info.svg";

const store = useToastStore();
const { toasts } = storeToRefs(store);

const getIcon = (type) => {
  switch (type) {
    case "success":
      return CheckCircleIcon;
    case "error":
      return XCircleIcon;
    case "warning":
      return ExclamationCircleIcon;
    default:
      return InformationCircleIcon;
  }
};

const getTypeClasses = (type) => {
  switch (type) {
    case "success":
      return "bg-[#ECFDF3] text-[#027A48] border-[#6CE9A6]";
    case "error":
      return "bg-[#FEF3F2] text-[#B42318] border-[#FEE4E2]";
    case "warning":
      return "bg-[#FFFAEB] text-[#B54708] border-[#FEF0C7]";
    default:
      return "bg-[#EFF8FF] text-[#1570EF] border-[#B2DDFF]";
  }
};
</script>

<template>
  <div
    class="fixed top-4 right-4 z-50 flex flex-col gap-2 min-w-[320px] max-w-[420px]"
  >
    <TransitionGroup name="toast" tag="div" class="space-y-2">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'flex items-start gap-3 p-4 rounded-lg border shadow-lg transform transition-all duration-300',
          getTypeClasses(toast.type),
        ]"
      >
        <!-- Icon -->
        <component
          :is="getIcon(toast.type)"
          class="w-5 h-5 flex-shrink-0 mt-0.5"
        />

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <h3 v-if="toast.title" class="font-semibold text-sm">
            {{ toast.title }}
          </h3>
          <p class="text-sm mt-1">{{ toast.message }}</p>
        </div>

        <!-- Close Button -->
        <button
          @click="store.removeToast(toast.id)"
          class="flex-shrink-0 hover:opacity-75 transition-opacity duration-200"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24">
            <path
              :class="
                toast.type === 'error' ? 'fill-[#B42318]' : 'fill-current'
              "
              d="M6.225 4.811a1 1 0 00-1.414 1.414L10.586 12 4.81 17.775a1 1 0 101.414 1.414L12 13.414l5.775 5.775a1 1 0 001.414-1.414L13.414 12l5.775-5.775a1 1 0 00-1.414-1.414L12 10.586 6.225 4.81z"
            />
          </svg>
        </button>

        <!-- Progress Bar -->
        <div
          class="absolute bottom-0 left-0 h-1 bg-white/20 transition-all duration-300"
          :style="{
            width: '100%',
            animation: `shrink ${toast.duration}ms linear forwards`,
          }"
        />
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes shrink {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}
</style>
