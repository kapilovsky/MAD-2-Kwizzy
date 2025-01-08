<template>
  <div class="min-h-screen bg-[#fafafa] p-8">
    <div><RouterLink to="/login">Back to Login</RouterLink></div>
    <div class="max-w-3xl mx-auto space-y-8">
      <div class="text-center mb-12">
        <h1 class="text-6xl font-bold sohne mb-4">Privacy Policy</h1>
        <p class="text-gray-600 sohne-mono">
          Updated: probably at some point 📅
        </p>
      </div>

      <section class="bg-white rounded-3xl p-8 shadow-sm">
        <h2 class="text-2xl font-bold mb-4 sohne">1. Data Security</h2>
        <p class="text-gray-700 leading-relaxed">Your data is protected by:</p>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mt-4">
          <li>A very intimidating "Keep Out" sign</li>
          <li>Black cat's watchful gaze</li>
          <li>
            State-of-the-art, bleeding edge sticky notes with "SECRET" written
            on them
          </li>
          <li>The power of friendship</li>
        </ul>
      </section>

      <section class="bg-white rounded-3xl p-8 shadow-sm">
        <h2 class="text-2xl font-bold mb-4 sohne">2. Third-Party Access</h2>
        <p class="text-gray-700 leading-relaxed">
          I don't share your data with third parties because I don't have any
          data to share. Also, I don't have any third parties. Or second
          parties. It's just me here.
        </p>
      </section>

      <section class="bg-white rounded-3xl p-8 shadow-sm">
        <h2 class="text-2xl font-bold mb-4 sohne">3. Your Rights</h2>
        <p class="text-gray-700 leading-relaxed">You have the right to:</p>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mt-4">
          <li>Request what data I have on you (none)</li>
          <li>Request data deletion (still none)</li>
          <li>Send me memes</li>
          <li>Give me a high five, if you like the project. :D</li>
        </ul>
      </section>

      <div class="text-center mt-12 p-8 bg-[#192227] rounded-3xl text-white">
        <p class="sohne-mono mb-4">Privacy Policy TL;DR ⚡️</p>
        <p class="text-gray-400">
          I respect your privacy so much that I don't even know how to collect
          your data. Rest assured, your secrets are safe with my incompetence.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
