import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import SubjectDetails from "@/views/Admin/Subject.vue";
import Chapter from "@/views/Admin/Chapter.vue";
import CreateQuiz from "@/views/Admin/CreateQuiz.vue";

const AdminRoutes = [
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
  },
  {
    path: "/admin",
    redirect: "/admin/dashboard",
  },
  {
    path: "/admin/subject/:id",
    name: "SubjectDetails",
    component: SubjectDetails,
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId",
    name: "Chapter",
    component: Chapter,
  },
  {
    path: "/admin/subject/:subjectId/chapter/:chapterId/quiz/create",
    name: "CreateQuiz",
    component: CreateQuiz,
  },
];

export default AdminRoutes;
