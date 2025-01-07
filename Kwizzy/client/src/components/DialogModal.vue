<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-lg max-w-md w-full mx-4">
      <!-- Header -->
      <div class="px-6 py-4 border-b">
        <h3 class="text-lg font-semibold">
          <slot name="title">Dialog Title</slot>
        </h3>
      </div>

      <!-- Content -->
      <div class="px-6 py-4">
        <slot name="content">Dialog content goes here</slot>
      </div>

      <!-- Actions -->
      <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end gap-2">
        <slot name="actions">
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            @click="$emit('confirm')"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Confirm
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(["close", "confirm"]);
</script>
