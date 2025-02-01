import { createRouter, createWebHistory } from "vue-router";
import AuthRoutes from "./Auth";
import { StudentRoutes, addNavigationGuards } from "./Student";
import AdminRoutes from "./Admin";

const routes = [...AuthRoutes, ...StudentRoutes, ...AdminRoutes];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Function to get user role from token
const getUserRole = () => {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role;
  } catch (error) {
    console.error("Error parsing token:", error);
    return null;
  }
};

// Navigation guard for authentication and authorization
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  const userRole = getUserRole();

  // If route requires auth and no token exists
  if (to.meta.requiresAuth && !token) {
    next("/login");
    return;
  }

  // Check for role-based access
  if (to.meta.requiresAuth && to.meta.roles) {
    // If route has specific roles requirement
    if (!to.meta.roles.includes(userRole)) {
      // If user's role isn't in the allowed roles
      if (userRole === "student") {
        next("/student/" + getUserId()); // Redirect to student dashboard
        return;
      } else if (userRole === "admin") {
        next("/admin/dashboard"); // Redirect to admin dashboard
        return;
      } else {
        next("/login"); // Fallback to login if role is invalid
        return;
      }
    }
  }

  // If trying to access admin routes
  if (to.path.startsWith("/admin") && userRole !== "admin") {
    next("/student/" + getUserId()); // Redirect to student dashboard
    return;
  }

  // If trying to access student routes as admin
  if (to.path.startsWith("/student") && userRole === "admin") {
    next("/admin/dashboard");
    return;
  }

  next();
});

router.afterEach((to, from) => {
  let title = to.meta.title || "Kwizzy";

  if (to.name === "quiz" && to.params.quizName) {
    title = `${to.params.quizName} | Kwizzy`;
  }

  document.title = title;

  if (history.pushState) {
    history.replaceState(history.state, title, window.location.href);
  }
});

function getUserId() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub || payload.id;
  } catch (error) {
    console.error("Error parsing token:", error);
    return null;
  }
}

addNavigationGuards(router);

export default router;
