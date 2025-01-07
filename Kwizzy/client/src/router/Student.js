import { useQuizStore } from "../stores/quizStore";
import { useQuizResultStore } from "../stores/quizResultStore";
import StudentLayout from "../views/Student/StudentLayout.vue";
import StudentDashboard from "../views/Student/StudentDashboard.vue";
const QuizDetails = () => import("../views/Student/Quiz.vue");
const QuizTaking = () => import("../views/Student/QuizTaking.vue");
const QuizResults = () => import("../views/Student/QuizResults.vue");
import ViewSubjects from "../views/Student/ViewSubjects.vue";
import Subject from "../views/Student/Subject.vue";

const StudentRoutes = [
  {
    path: "/student/:id",
    name: "student",
    component: StudentLayout,
    meta: {
      requiresAuth: true,
      title: "Student Dashboard",
      roles: ['student']
    },
    children: [
      {
        path: "",
        component: StudentDashboard,
        name: "student-dashboard",
        meta: {
          requiresAuth: true,
          title: "Student Dashboard",
        },
      },
      {
        path: "subjects",
        name: "ViewSubjects",
        component: ViewSubjects,
        meta: {
          requiresAuth: true,
          title: "Subjects",
        },
      },
      {
        path: "subject/:subjectId",
        name: "subject",
        component: Subject,
        meta: {
          requiresAuth: true,
          title: "Subject Details",
        },
      },
      {
        path: "quiz/:quizId",
        name: "quiz",
        component: QuizDetails,
        meta: {
          requiresAuth: true,
          title: "Quiz Details",
        },
      },
      {
        path: "quiz/:quizId/take",
        name: "quiz-take",
        component: QuizTaking,
        meta: {
          requiresAuth: true,
          title: "Taking Quiz",
          preventRefresh: true, // to handle refresh warnings
        },
        beforeEnter: async (to, from, next) => {
          const quizStore = useQuizStore();

          try {
            // Check if quiz is in progress
            const quizStartTime = localStorage.getItem("quizStartTime");
            const isInProgress =
              quizStartTime &&
              (await quizStore.checkQuizStatus(to.params.quizId));

            if (!isInProgress && from.name !== "quiz") {
              // If quiz is not in progress and not coming from quiz details page
              next({
                name: "quiz",
                params: {
                  id: to.params.id,
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
        path: "quiz/:quizId/results",
        name: "quiz-results",
        component: QuizResults,
        meta: {
          requiresAuth: true,
          title: "Quiz Results",
          preventRefresh: true,
        },
        beforeEnter: async (to, from, next) => {
          const quizResultStore = useQuizResultStore();

          try {
            // If coming from quiz-take, we already have the result
            if (from.name === "quiz-take") {
              next();
              return;
            }

            // If refreshing or direct access, check if we have resultId
            const resultId = to.query.resultId;
            if (!resultId) {
              next({
                name: "student",
                params: { id: to.params.id },
              });
              return;
            }

            // Pre-fetch the result
            await quizResultStore.fetchResult(resultId);
            next();
          } catch (error) {
            console.error("Error fetching quiz result:", error);
            next({ name: "error" });
          }
        },
      },
    ],
  },
];

// Add navigation guards
const addNavigationGuards = (router) => {
  // Clean up when leaving quiz-related routes
  router.afterEach((to, from) => {
    if (from.name === "quiz-take" && to.name !== "quiz-results") {
      // Clear quiz data if leaving quiz without completing
      localStorage.removeItem("quizStartTime");
      localStorage.removeItem("totalDuration");
      const quizStore = useQuizStore();
      quizStore.resetQuiz();
    }
  });
};

export { StudentRoutes, addNavigationGuards };
