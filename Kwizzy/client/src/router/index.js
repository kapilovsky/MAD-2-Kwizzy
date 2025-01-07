import { createRouter, createWebHistory } from "vue-router";
import AuthRoutes from "./Auth";
import StudentRoutes from "./Student";
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

export default router;
