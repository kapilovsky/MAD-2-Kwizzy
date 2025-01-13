<template>
  <div
    class="min-h-screen flex py-24 justify-center bg-gray-50 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <RouterLink
        to="/login"
        class="text-gray-700 sohne-mono text-xs hover:text-[#0000ff]"
      >
        Back to Login
      </RouterLink>
      <header class="flex items-center gap-8 justify-center">
        <img
          class="h-12 w-auto mix-blend-difference"
          :src="logo"
          alt="Workflow"
        />

        <h1 class="text-2xl font-bold tracking-tighter">Kwizzy</h1>
      </header>
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Forgot Password
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Enter your email address and we'll send you a link to reset your
          password.
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input
              id="email-address"
              v-model="email"
              name="email"
              type="email"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Loader v-if="isLoading" class="mix-blend-exclusion" />
            {{ isLoading ? "Sending..." : "Send Reset Link" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import logo from "../assets/images/landing-page/white logo.png";
import { useToast } from "@/composables/useToast";
const toast = useToast();

const API_URL = import.meta.env.VITE_API_URL;

const email = ref("");
const isLoading = ref(false);

const handleSubmit = async () => {
  try {
    isLoading.value = true;

    const response = await axios.post(`${API_URL}/auth/forgot-password`, {
      email: email.value,
    });
    toast.success(response.data.message);
    email.value = "";
  } catch (error) {
    toast.error(error.response?.data?.error || "Failed to process request");
  } finally {
    isLoading.value = false;
  }
};
</script>
