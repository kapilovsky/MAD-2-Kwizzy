<script setup>
import signup from "../assets/images/login-signup/Signup.jpg";
import { RouterLink, useRouter } from "vue-router";
import axios from "axios";
import { ref } from "vue";

const name = ref("");
const email = ref("");
const dob = ref("");
const qualification = ref("");
const password = ref("");
// const role = ref("");
const API_URL = import.meta.env.VITE_API_URL;

const router = useRouter();

const submit = async () => {
  // Basic validation
  if (
    !name.value ||
    !email.value ||
    !dob.value ||
    !qualification.value ||
    !password.value
  ) {
    alert("Please fill out all fields!");
    return;
  }

  // Make an API call to authenticate
  try {
    const response = await axios.post(`${API_URL}/register`, {
      name: name.value,
      email: email.value,
      dob: dob.value,
      qualification: qualification.value,
      // role: role.value,
      password: password.value,
    });
    if (response.data) {
      console.log("Registration successful:", response.data);
      router.push("/login");
    }
  } catch (error) {
    console.error("Error signing up:", error.response?.data || error);
    alert(error.response?.data?.message || "Error during registration");
  }
};
</script>

<template>
  <div class="container flex items-center justify-between h-screen px-24">
    <div
      class="Signup flex flex-col justify-start gap-4 h-full py-10 max-w-sm ml-12"
    >
      <h1 class="text-4xl">Ready to Crush Quizzes Like a Pro?</h1>

      <form @submit.prevent="submit" class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="name">Name</label>
          <input
            v-model="name"
            type="text"
            name="name"
            id="name"
            placeholder="Your Name"
            required
          />
        </div>

        <div class="flex flex-col gap-1">
          <label for="email">Email</label>
          <input
            v-model="email"
            type="email"
            name="email"
            id="email"
            placeholder="Example@email.com"
            required
          />
        </div>

        <div class="flex flex-col gap-1">
          <label for="dob">Date of Birth</label>
          <input v-model="dob" type="date" name="dob" id="dob" required />
        </div>

        <!-- <div class="flex flex-col gap-1">
          <label for="role">Role</label>
          <input v-model="role" type="text" name="role" id="role" required />
        </div> -->

        <div class="flex flex-col gap-1">
          <label for="qualification"> Qualification</label>
          <select
            v-model="qualification"
            name="qualification"
            id="qualification"
            required
          >
            <option value="">Select Your Qualification</option>
            <option value="school">High School</option>
            <option value="undergrad">Undergraduate</option>
            <option value="postgrad">Postgraduate</option>
            <option value="working">Working Professional</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="flex flex-col gap-1">
          <label for="password">Password</label>
          <input
            v-model="password"
            type="password"
            name="password"
            id="password"
            placeholder="At least 8 characters"
            required
          />
        </div>

        <p>
          Already have an account?
          <RouterLink to="/login"
            ><span class="text-blue-700 hover:underline login"
              >Login</span
            ></RouterLink
          >
        </p>

        <button
          class="py-[10px] font-medium text-white bg-black rounded-lg hover:bg-black/90 transition-all ease-linear active:scale-95 flex items-center justify-center gap-2"
          type="submit"
        >
          Sign Up <ion-icon name="arrow-forward-sharp"></ion-icon>
        </button>
      </form>

      <footer class="mt-4">
        <p>
          By signing up, you agree to our
          <span class="text-blue-600">Terms of Service</span> and
          <span class="text-blue-600">Privacy Policy</span>.
        </p>
      </footer>
    </div>
    <div class="login-image">
      <div class="img-wrapper w-[720px]">
        <img class="rounded-2xl" :src="signup" alt="" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1800px;
  margin: 0 auto;
}

.Signup h1 {
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

form select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  border-radius: 6px;
}

.login {
  font-family: Instrument Serif;
  font-weight: 600;
  font-style: italic;
  font-size: 17px;
}

button[type="submit"] ion-icon {
  font-size: 18px;
  transform: translateX(-4px);
  opacity: 0;
  transition: all 0.2s ease;
}

button[type="submit"]:hover ion-icon {
  opacity: 1;
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>
