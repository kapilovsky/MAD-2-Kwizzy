const AdminDashboard = () => import("@/views/Admin/AdminDashboard.vue");

const AdminRoutes = [
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
  },
];

export default AdminRoutes;
