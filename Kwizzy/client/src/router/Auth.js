import LandingPage from "../views/LandingPage.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
const PageNotFound = () => import("../views/404.vue");

const AuthRoutes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/:catchAll(.*)",
    name: "Page Not Found",
    component: PageNotFound,
  },
];

export default AuthRoutes;
