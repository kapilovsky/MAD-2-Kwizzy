import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import Subject from "@/views/Admin/Subject.vue";
import Chapter from "@/views/Admin/Chapter.vue";
const Users = () =>
  import(/* webpackPrefetch: true */ "@/views/Admin/Users.vue");
const Quiz = () => import(/* webpackPrefetch: true */ "@/views/Admin/Quiz.vue");
const CreateQuiz = () =>
  import(/* webpackPrefetch: true */ "@/views/Admin/CreateQuiz.vue");
const EditQuiz = () =>
  import(/* webpackPrefetch: true */ "@/views/Admin/EditQuiz.vue");
const StudentDetails = () => import("@/views/Admin/StudentDetails.vue");

const AdminRoutes = [
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    redirect: "/admin/dashboard",
  },
  {
    path: "/admin/subject/:id",
    name: "Subject",
    component: Subject,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId",
    name: "Chapter",
    component: Chapter,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/users",
    name: "Users",
    component: Users,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId/quiz/create",
    name: "CreateQuiz",
    component: CreateQuiz,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId/quiz/:quizId",
    name: "Quiz",
    component: Quiz,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId/quiz/:quizId/edit",
    name: "EditQuiz",
    component: EditQuiz,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/student/:id",
    name: "StudentDetails",
    component: StudentDetails,
    meta: { requiresAuth: true },
  },
];

export default AdminRoutes;
