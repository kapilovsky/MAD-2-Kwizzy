const Login = () => import("../views/Login.vue");
const Signup = () => import("../views/Signup.vue");
const LandingPage = () => import("../views/LandingPage.vue");

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
];

export default AuthRoutes;
