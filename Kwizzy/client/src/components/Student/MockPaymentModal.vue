<!-- components/MockPaymentModal.vue -->
<template>
  <DialogModal @close="$emit('close')">
    <template #title>
      <span class="text-xl font-bold">Payment Details</span>
    </template>
    <template #content>
      <div class="space-y-4">
        <div class="bg-white p-4 rounded-lg">
          <div class="flex justify-between items-center">
            <span class="text-gray-600 font-medium tracking-tighter"
              >Amount to Pay:</span
            >
            <span class="text-xl font-bold text-gray-800">₹{{ amount }}</span>
          </div>
        </div>

        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-900 mb-1">
              Card Number
            </label>
            <input
              type="text"
              v-model="cardNumber"
              placeholder="4111111111111111"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-orange-500 focus:border-orange-500 outline-none"
              maxlength="16"
              minlength="16"
            />
            <p class="text-xs text-gray-500 mt-1">
              Use 4111111111111111 for testing
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Expiry Date
              </label>
              <input
                type="text"
                v-model="expiry"
                placeholder="MM/YY"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-orange-500 focus:border-orange-500 outline-none"
                maxlength="5"
                minlength="5"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                CVV
              </label>
              <input
                type="text"
                v-model="cvv"
                placeholder="123"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-orange-500 focus:border-orange-500 outline-none"
                maxlength="3"
                minlength="3"
              />
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <button
        @click="$emit('close')"
        class="px-4 py-2 text-gray-600 font-semibold hover:text-gray-800 mt-4"
        :disabled="isProcessing"
      >
        Cancel
      </button>
      <button
        @click="processPayment"
        :disabled="!isFormValid || isProcessing"
        class="px-6 py-2 bg-orange-500 text-white rounded-xl hover:bg-orange-600 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold flex items-center gap-2 mt-4"
      >
        <span v-if="isProcessing" class="animate-spin">↻</span>
        {{ isProcessing ? "Processing..." : "Pay Now" }}
      </button>
    </template>
  </DialogModal>
</template>

<script setup>
import { ref, computed } from "vue";
import DialogModal from "../DialogModal.vue";

const props = defineProps({
  amount: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["close", "success"]);

const cardNumber = ref("");
const expiry = ref("");
const cvv = ref("");
const isProcessing = ref(false);

const isFormValid = computed(() => {
  return (
    cardNumber.value.length === 16 &&
    expiry.value.length === 5 &&
    cvv.value.length === 3
  );
});

const processPayment = async () => {
  try {
    isProcessing.value = true;

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Test card validation
    if (cardNumber.value !== "4111111111111111") {
      throw new Error("Invalid test card. Please use: 4111 1111 1111 1111");
    }

    emit("success", {
      transactionId:
        "Kw133y_" +
        Date.now().toString(36) +
        Math.random().toString(36).slice(2),
      amount: props.amount,
    });
  } catch (error) {
    alert(error.message);
  } finally {
    isProcessing.value = false;
  }
};
</script>
