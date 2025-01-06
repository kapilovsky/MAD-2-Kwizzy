const StudentDashboard = () => import("../views/Student/StudentDashboard.vue");
const QuizDetails = () => import("../views/Student/Quiz.vue");

const StudentRoutes = [
  {
    path: "/student/:id",
    name: "student",
    component: StudentDashboard,
  },
  {
    path: "/student/:id/quiz/:quizId",
    name: "quiz",
    component: QuizDetails,
  },
];

export default StudentRoutes;
