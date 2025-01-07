import LandingPage from "../views/LandingPage.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
const PageNotFound = () => import("../views/404.vue");

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
    path: "/:catchAll(.*)",
    name: "Page Not Found",
    component: PageNotFound,
    meta: { title: "404 Page Not Found" },
  },
];

export default AuthRoutes;
