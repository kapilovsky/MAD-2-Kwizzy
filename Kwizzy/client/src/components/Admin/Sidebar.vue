<!-- components/Sidebar/Sidebar.vue -->
<script setup>
import { ref, provide } from "vue";
import { useRouter } from "vue-router";
import logo from "../../assets/images/landing-page/white logo.png";
const router = useRouter();
const isOpen = ref(false);
const isMobileOpen = ref(false);

import HomeIcon from "../../assets/images/icons/home.svg";
import QuizIcon from "../../assets/images/icons/quiz.svg";
import UsersIcon from "../../assets/images/icons/users.svg";
import ChartBarIcon from "../../assets/images/icons/summary.svg";
import LogoutIcon from "../../assets/images/icons/logout.svg";
import SearchIcon from "../../assets/images/icons/search.svg";
import MenuIcon from "../../assets/images/icons/menu.svg";
import CloseIcon from "../../assets/images/icons/close.svg";

provide("sidebarState", {
  isOpen,
  isMobileOpen,
  toggleSidebar: () => (isOpen.value = !isOpen.value),
  toggleMobileSidebar: () => (isMobileOpen.value = !isMobileOpen.value),
});

const navigationItems = [
  { name: "Home", icon: HomeIcon, path: "/admin" },
  { name: "Quizzes", icon: QuizIcon, path: "/admin/quizzes" },
  { name: "Users", icon: UsersIcon, path: "/admin/users" },
  { name: "Summary", icon: ChartBarIcon, path: "/admin/summary" },
];

const handleLogout = () => {
  // Implement logout logic
  router.push("/login");
};
</script>

<template>
  <div class="flex h-screen bg-[#fafafa]">
    <!-- Desktop Sidebar -->
    <Transition>
      <aside
        class="hidden md:flex flex-col bg-[#fafafa] overflow-hidden transition-all duration-300 ease-in-out"
        :class="[isOpen ? 'w-64' : 'w-16']"
        @mouseenter="isOpen = true"
        @mouseleave="isOpen = false"
      >
        <!-- Logo Section -->
        <div class="h-16 flex items-center px-4 bg-[#fafafa]">
          <img :src="logo" alt="Logo" class="w-8 h-8 mix-blend-difference" />
          <Transition name="fade">
            <span v-if="isOpen" class="ml-3 text-neutral-700 font-bold text-lg">
              Kwizzy
            </span>
          </Transition>
        </div>

        <!-- Navigation Links -->
        <nav class="flex-1 px-2 py-4 space-y-2">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.path"
            class="flex items-center px-3 py-2 text-neutral-900 rounded-md hover:translate-x-2 group transition-all duration-200"
            :class="{ 'bg-[#f1f1f1]': $route.path === item.path }"
          >
            <component
              :is="item.icon"
              class="w-6 h-6"
              :class="{ 'text-neutral-900': $route.path === item.path }"
            />
            <Transition name="fade">
              <span
                v-if="isOpen"
                class="ml-3 whitespace-nowrap text-sm font-semibold"
              >
                {{ item.name }}
              </span>
            </Transition>
          </router-link>

          <!-- Logout Button -->
          <button
            @click="handleLogout"
            class="w-full flex items-center px-3 py-2 text-neutral-900 rounded-lg hover:translate-x-2 transition-all duration-200"
          >
            <LogoutIcon class="w-6 h-6" />
            <Transition name="fade">
              <span v-if="isOpen" class="ml-3 text-sm font-semibold"
                >Logout</span
              >
            </Transition>
          </button>
        </nav>
      </aside>
    </Transition>

    <!-- Mobile Sidebar -->
    <div class="md:hidden bg-[#fafafa]">
      <button
        @click="isMobileOpen = true"
        class="fixed top-5 left-2 z-40 text- gray-700 hover:bg-gray-200 rounded-lg"
      >
        <component :is="MenuIcon" class="w-6 h-6" />
      </button>

      <Transition name="slide">
        <div
          v-if="isMobileOpen"
          class="fixed inset-0 z-50 bg-gray-100/50 backdrop-blur-sm"
          @click="isMobileOpen = false"
        >
          <div class="fixed inset-y-0 left-0 w-64 bg-[#fafafa] p-6" @click.stop>
            <!-- Mobile Navigation -->
            <div class="flex justify-between items-center mb-8">
              <img
                :src="logo"
                alt="Logo"
                class="w-8 h-8 mix-blend-difference"
              />
              <button
                @click="isMobileOpen = false"
                class="p-2 text-gray-700 hover:translate-x-2 rounded-lg"
              >
                <component :is="CloseIcon" class="w-6 h-6" />
              </button>
            </div>

            <nav class="space-y-2">
              <!-- Same navigation items as desktop -->
              <router-link
                v-for="item in navigationItems"
                :key="item.name"
                :to="item.path"
                class="flex items-center px-2 py-2 text-gray-700 rounded-md group transition-colors duration-200"
                :class="{ 'bg-gray-200': $route.path === item.path }"
                @click="isMobileOpen = false"
              >
                <component
                  :is="item.icon"
                  class="w-6 h-6"
                  :class="{ 'text-gray-900': $route.path === item.path }"
                />
                <span class="ml-3 text-sm font-semibold">{{ item.name }}</span>
              </router-link>
              <!-- Logout Button -->
              <button
                @click="handleLogout"
                class="w-full flex items-center px-3 py-2 text-neutral-900 rounded-lg hover:translate-x-2 transition-all duration-200"
              >
                <LogoutIcon class="w-6 h-6" />
                <Transition name="fade">
                  <span class="ml-3 text-sm font-semibold">Logout</span>
                </Transition>
              </button>
            </nav>
          </div>
        </div>
      </Transition>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Navigation Bar -->
      <header
        class="h-16 bg-white flex items-center justify-between px-6 gap-6"
      >
        <div class="flex items-center flex-1">
          <div class="ml-4 flex-1 max-w-lg">
            <div class="relative">
              <component
                :is="SearchIcon"
                class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
              />
              <input
                type="text"
                placeholder="Search "
                class="w-full pl-10 pr-4 py-2 bg-gray-100 text-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
              />
            </div>
          </div>
        </div>

        <!-- Right Side Icons -->
        <div class="flex items-center">
          <div class="flex items-center gap-4">
            <img
              :src="logo"
              alt="User avatar"
              class="w-8 h-8 rounded-full mix-blend-difference"
            />
            <span class="text-sm font-medium text-gray-700">Admin</span>
          </div>
        </div>
      </header>

      <!-- Main Content Area -->
      <main class="flex-1 overflow-y-auto bg-white p-6">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1f2937;
}

::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

header {
  border-radius: 10px 0px 0px 0px;
  border-left: 2px solid #e5e7ebd6;
  border-top: 2px solid #e5e7ebd6;
}

main {
  border-left: 2px solid #e5e7ebd6;
}
</style>
