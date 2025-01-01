<script setup>
import signup from "../assets/images/login-signup/Signup.jpg";
import { RouterLink } from "vue-router";

import { ref } from "vue";

const email = ref("");
const password = ref("");
const rememberMe = ref(false);

const handleLogin = () => {
  // Basic validation
  if (!email.value || !password.value) {
    alert("Please fill out all fields!");
    return;
  }

  // Make an API call to authenticate
  console.log({
    email: email.value,
    password: password.value,
    rememberMe: rememberMe.value,
  });

  alert("Login attempt submitted! Replace with actual logic.");
};
</script>

<template>
  <div class="container flex items-center justify-between h-screen px-24">
    <div
      class="Signup flex flex-col justify-start gap-4 h-full py-10 max-w-sm ml-12"
    >
      <h1 class="text-4xl">Ready to Crush Quizzes Like a Pro?</h1>

      <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="name">Name</label>
          <input type="text" name="name" id="name" placeholder="Your Name" />
        </div>

        <div class="flex flex-col gap-1">
          <label for="email">Email</label>
          <input
            type="email"
            name="email"
            id="email"
            placeholder="Example@email.com"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label for="email">Date of Birth</label>
          <input type="date" name="dob" id="dob" />
        </div>

        <div class="flex flex-col gap-1">
          <label for="qualification"> Qualification</label>
          <select name="qualification" id="qualification">
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
            type="password"
            name="password"
            id="password"
            placeholder="At least 8 characters"
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
