const StudentDashboard = () => import("../views/Student/StudentDashboard.vue");
const QuizDetails = () => import("../views/Student/Quiz.vue");
const QuizTaking = () => import("../views/Student/QuizTaking.vue");
const QuizResults = () => import("../views/Student/QuizResults.vue");

const StudentRoutes = [
  {
    path: "/student/:id",
    name: "student",
    component: StudentDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/student/:id/quiz/:quizId",
    name: "quiz",
    component: QuizDetails,
    meta: { requiresAuth: true },
  },
  {
    path: "/student/:id/quiz/:quizId/take",
    name: "quiz-take",
    component: QuizTaking,
    meta: { requiresAuth: true },
    
  },
  {
    path: "/student/:id/quiz/:quizId/results",
    name: "quiz-results",
    component: QuizResults,
    meta: { requiresAuth: true },
    
  },
];

export default StudentRoutes;
