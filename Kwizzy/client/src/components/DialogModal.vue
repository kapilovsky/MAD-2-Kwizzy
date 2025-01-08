<template>
  <div
    class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center sm:justify-center z-50"
  >
    <div
      class="bg-[#fff9f0] text-orange-600 rounded-3xl sm:w-[700px] w-[400px]"
    >
      <!-- Header -->
      <div class="sm:px-6 px-4 pt-4 pb-2">
        <h3 class="text-3xl tracking-tighter font-bold">
          <slot name="title">Dialog Title</slot>
        </h3>
      </div>

      <!-- Content -->
      <div class="sm:px-6 px-4 py-2">
        <slot name="content">Dialog content goes here</slot>
      </div>

      <!-- Actions -->
      <div
        class="sm:px-6 px-4 py-4 pt-0 bg-[#fff9f0] rounded-3xl flex justify-end gap-2"
      >
        <slot name="actions">
          <button @click="$emit('close')">Cancel</button>
          <button @click="$emit('confirm')">Confirm</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(["close", "confirm"]);
</script>
