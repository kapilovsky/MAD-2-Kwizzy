<template>
  <div class="min-h-screen bg-[#fafafa] p-8">
    <div><RouterLink to="/login">Back to Login</RouterLink></div>
    <div class="max-w-3xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-6xl font-bold sohne mb-4">Terms of Service</h1>
        <p class="text-gray-600 sohne-mono">Last updated: idk</p>
      </div>

      <div class="space-y-8">
        <section class="bg-white rounded-3xl p-8 shadow-sm">
          <h2 class="text-2xl font-bold mb-4 sohne">1. Acceptance of Terms</h2>
          <p class="text-gray-700 leading-relaxed">
            By accessing this website, you hereby accept that this is just a
            project and these terms are completely made up. You also agree to
            occasionally laugh at my jokes, even if they're not funny. It's just
            polite, really.
          </p>
        </section>

        <section class="bg-white rounded-3xl p-8 shadow-sm">
          <h2 class="text-2xl font-bold mb-4 sohne">
            2. User Responsibilities
          </h2>
          <p class="text-gray-700 leading-relaxed mb-4">
            Users are responsible for:
          </p>
          <ul class="list-disc list-inside space-y-2 text-gray-700">
            <li>Not falling asleep during quizzes (I can tell 👀)</li>
            <li>Pretending to read these terms of service</li>
            <li>Not using "dog ate my homework" excuse (get creative!)</li>
            <li>Maintaining a sense of humor at all times</li>
          </ul>
        </section>

        <section class="bg-white rounded-3xl p-8 shadow-sm">
          <h2 class="text-2xl font-bold mb-4 sohne">
            3. Intellectual Property
          </h2>
          <p class="text-gray-700 leading-relaxed">
            All content is powered by ✨ magic ✨ and 4:00 AM coding sessions.
            Any resemblance to actual intellectual property is purely
            coincidental and probably because I watched too many coding
            tutorials.
          </p>
        </section>

        <section class="bg-white rounded-3xl p-8 shadow-sm">
          <h2 class="text-2xl font-bold mb-4 sohne">4. Termination</h2>
          <p class="text-gray-700 leading-relaxed">
            I reserve the right to terminate your access if you don't laugh at
            my jokes. Just kidding! (or am I? 👺)
          </p>
        </section>

        <section class="bg-white rounded-3xl p-8 shadow-sm">
          <h2 class="text-2xl font-bold mb-4 sohne">5. Changes to Terms</h2>
          <p class="text-gray-700 leading-relaxed">
            These terms may change whenever I feeling particularly creative or I
            may never even look at them again after this project is built.
          </p>
        </section>

        <div class="text-center mt-12 p-8 bg-[#192227] rounded-3xl text-white">
          <p class="sohne-mono mb-4">Congratulations! 🎉</p>
          <p class="text-gray-400">
            You've reached the end of my terms. This is probably the first time
            anyone has ever read them. You deserve a cookie 🍪 (not the tracking
            kind, just a real one).
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
