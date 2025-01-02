const StudentDashboard = () => import("../views/Student/StudentDashboard.vue");

const StudentRoutes = [
  {
    path: "/student",
    name: "student",
    component: StudentDashboard,
  },
];

export default StudentRoutes;