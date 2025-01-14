<script setup>
import login from "../assets/images/login-signup/Login.jpg";
import { RouterLink, useRouter } from "vue-router";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
import { ref } from "vue";
const router = useRouter();

const email = ref("");
const password = ref("");

const handleLogin = async () => {
  // Basic validation
  if (!email.value || !password.value) {
    alert("Please fill out all fields!");
    return;
  }

  // Make an API call to authenticate
  try {
    const response = await axios.post(`${API_URL}/login`, {
      email: email.value,
      password: password.value,
    });
    const { access_token, refresh_token, user_role, message, user_id } =
      response.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    if (user_role == "admin") {
      router.push("/admin/dashboard");
    } else if (user_role === "student") {
      router.push(`/student/${user_id}`);
    }
    console.log(message);
  } catch (error) {
    console.error("Error logging in:", error);
    alert(error.response?.data?.message || "Error during login");
  }
};
</script>

<template>
  <div
    class="container bg-white flex items-center sm:justify-between h-screen px-24"
  >
    <div
      class="login flex flex-col justify-start gap-6 h-full py-24 max-w-sm sm:ml-12 px-8 sm:px-0"
    >
      <h1 class="text-4xl">Welcome Back 👋</h1>
      <p class="font-[Inter] text-black/70 text-lg">
        Please login to access you account
      </p>

      <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
        <div class="flex flex-col gap-2">
          <label for="email">Email</label>
          <input
            type="email"
            name="email"
            id="email"
            placeholder="Example@email.com"
            v-model="email"
          />
        </div>

        <div class="flex flex-col gap-2">
          <label for="password">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            placeholder="At least 8 characters"
            v-model="password"
          />
        </div>

        <RouterLink
          to="/forgot-password"
          class="text-sm text-blue-600 hover:underline tracking-tighter text-right"
          >Forgot password?</RouterLink
        >

        <p>
          No account?
          <RouterLink to="/signup"
            ><span class="text-blue-700 hover:underline signup"
              >Sign up</span
            ></RouterLink
          >
        </p>

        <button
          class="py-[10px] font-medium text-white bg-black rounded-lg hover:bg-black/90 transition-all ease-linear active:scale-95 flex items-center justify-center gap-2 group"
          type="submit"
        >
          Login <span>🡲</span>
        </button>
      </form>

      <footer class="mt-24">
        <p>
          By logging in, you agree to my
          <RouterLink
            class="text-blue-600 hover:underline"
            to="/terms-of-service"
            >Terms of Service</RouterLink
          >
          and
          <RouterLink class="text-blue-600 hover:underline" to="/privacy-policy"
            >Privacy Policy</RouterLink
          >.
        </p>
      </footer>
    </div>
    <div class="login-image">
      <div class="img-wrapper w-[720px]">
        <img class="rounded-2xl" :src="login" alt="" />
      </div>
      <div></div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1800px;
  margin: 0 auto;
}

.login h1 {
  font-family: Inter;
  font-weight: 700;
  letter-spacing: -1.25px;
}

form input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  border-radius: 6px;
}

.signup {
  font-family: Instrument Serif;
  font-weight: 600;
  font-style: italic;
  font-size: 17px;
}

button[type="submit"] span {
  font-size: 18px;
  transform: translateX(-4px);
  opacity: 0;
  transition: all 0.2s ease;
}

button[type="submit"]:hover span {
  opacity: 1;
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
  .login-image {
    display: none;
  }
}
</style>
