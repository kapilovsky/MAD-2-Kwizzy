const AdminDashboard = () => import("@/views/Admin/AdminDashboard.vue");
const SubjectDetails = () => import("@/views/Admin/SubjectDetails.vue");

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
];

export default AdminRoutes;
