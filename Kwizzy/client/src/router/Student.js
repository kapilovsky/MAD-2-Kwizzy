import { useQuizStore } from "../stores/quizStore";
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
    meta: {
      requiresAuth: true,
      title: "Taking Quiz",
    },
    beforeEnter: async (to, from, next) => {
      const quizStore = useQuizStore();

      try {
        // Check if quiz is in progress
        const isInProgress = await quizStore.checkQuizStatus(to.params.quizId);

        if (!isInProgress && from.name !== "quiz") {
          // If quiz is not in progress and not coming from quiz details page
          next({
            name: "quiz",
            params: {
              studentId: to.params.studentId,
              quizId: to.params.quizId,
            },
          });
          return;
        }

        next();
      } catch (error) {
        console.error("Error checking quiz status:", error);
        next({ name: "error" });
      }
    },
  },
  {
    path: "/student/:id/quiz/:quizId/results",
    name: "quiz-results",
    component: QuizResults,
    meta: { requiresAuth: true },
  },
];

export default StudentRoutes;
