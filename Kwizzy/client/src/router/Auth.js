import LandingPage from "../views/LandingPage.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
const PageNotFound = () => import("../views/404.vue");
const Unauthorized = () => import("../views/Unauthorized.vue");

const AuthRoutes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
    meta: { title: "Kwizzy" },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { title: "Login" },
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
    meta: { title: "Signup" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "Page Not Found",
    component: PageNotFound,
    meta: { title: "404 Page Not Found" },
  },

  {
    path: "/unauthorized",
    name: "unauthorized",
    component: () => import("@/views/Unauthorized.vue"),
    meta: {
      title: "Unauthorized Access",
    },
  },
];

export default AuthRoutes;
