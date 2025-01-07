import { createRouter, createWebHistory } from "vue-router";
import AuthRoutes from "./Auth";
import { StudentRoutes, addNavigationGuards } from "./Student";
import AdminRoutes from "./Admin";

const routes = [...AuthRoutes, ...StudentRoutes, ...AdminRoutes];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem("access_token")) {
    next("/login");
  } else {
    next();
  }
});
router.afterEach((to, from) => {
  // Basic title
  let title = to.meta.title || "Kwizzy";

  // For quiz-specific routes, you can make the title more specific
  if (to.name === "quiz" && to.params.quizName) {
    title = `${to.params.quizName} | Kwizzy`;
  }

  // Update document title
  document.title = title;

  // Update browser history entry
  if (history.pushState) {
    history.replaceState(history.state, title, window.location.href);
  }
});

addNavigationGuards(router);

export default router;
