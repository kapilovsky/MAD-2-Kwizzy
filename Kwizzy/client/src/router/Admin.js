import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import SubjectDetails from "@/views/Admin/SubjectDetails.vue";
import Chapter from "@/views/Admin/Chapter.vue";

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
];

export default AdminRoutes;
