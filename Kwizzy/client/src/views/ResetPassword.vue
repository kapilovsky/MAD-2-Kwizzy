<!-- views/ResetPassword.vue -->
<template>
  <div
    class="min-h-screen flex py-24 justify-center bg-gray-50 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
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
          Reset Password
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Enter your new password below
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class=" flex flex-col gap-4">
          <div>
            <label for="password" class="sr-only">New Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              minlength="8"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="New password"
            />
          </div>
          <div>
            <label for="confirm-password" class="sr-only"
              >Confirm Password</label
            >
            <input
              id="confirm-password"
              v-model="confirmPassword"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Confirm password"
            />
            <p
              v-if="password.length < 8"
              class="text-red-600 tracking-tighter text-xs mt-2"
            >
              Password must be at least 8 characters long.
            </p>
            <p
              v-if="password !== confirmPassword"
              class="text-red-600 tracking-tighter text-xs mt-2"
            >
              Passwords do not match.
            </p>
          </div>
        </div>

        <Loader v-if="isLoading" />

        <div>
          <button
            type="submit"
            :disabled="isLoading || !isValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {{ isLoading ? "Resetting..." : "Reset Password" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import Loader from "@/components/Loader.vue";
import logo from "../assets/images/landing-page/white logo.png";

import { useToast } from "@/composables/useToast";
const toast = useToast();

const route = useRoute();
const router = useRouter();

const password = ref("");
const confirmPassword = ref("");
const isLoading = ref(false);

const isValid = computed(() => {
  return password.value.length >= 8 && password.value === confirmPassword.value;
});

const handleSubmit = async () => {
  try {
    isLoading.value = true;

    const token = route.query.token;
    if (!token) {
      throw new Error("Reset token is missing");
    }

    await axios.post(`${API_URL}/auth/reset-password`, {
      token,
      new_password: password.value,
    });

    toast.success("Password reset successful! Redirecting to login...");

    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (error) {
    toast.error(error.response?.data?.error || "Failed to reset password");
  } finally {
    isLoading.value = false;
  }
};
</script>
