import { createRouter, createWebHistory } from "vue-router";
import AuthRoutes from "./Auth";
import StudentRoutes from "./Student";
import AdminRoutes from "./Admin";

const routes = [...AuthRoutes, ...StudentRoutes, ...AdminRoutes];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
