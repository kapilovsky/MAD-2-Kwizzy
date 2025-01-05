const StudentDashboard = () => import("../views/Student/StudentDashboard.vue");

const StudentRoutes = [
  {
    path: "/student/:id",
    name: "student",
    component: StudentDashboard,
  },
];

export default StudentRoutes;
