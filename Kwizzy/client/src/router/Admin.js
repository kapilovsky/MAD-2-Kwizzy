const AdminDashboard = () => import("@/views/Admin/AdminDashboard.vue");
const SubjectDetails = () => import("@/views/Admin/SubjectDetails.vue");

const AdminRoutes = [
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
  },
  {
    path: "/admin/subject/:id",
    name: "SubjectDetails",
    component: SubjectDetails,
  },
];

export default AdminRoutes;
