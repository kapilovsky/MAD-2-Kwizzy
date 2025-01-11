// stores/subjectStore.js
import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { cache } from "@/utils/cache";
import { useToast } from "@/composables/useToast";

export const useSubjectStore = defineStore("subjects", () => {
  const allSubjects = ref([]);
  const isLoading = ref(false);
  const loadingTimeout = ref(null);
  const toast = useToast();

  const startLoading = () => {
    loadingTimeout.value = setTimeout(() => {
      isLoading.value = true;
    }, 200);
  };

  const stopLoading = () => {
    if (loadingTimeout.value) {
      clearTimeout(loadingTimeout.value);
    }
    isLoading.value = false;
  };

  const fetchSubjects = async (force = false) => {
    const CACHE_KEY = "subjects_data";

    if (!force) {
      const cachedData = cache.get(CACHE_KEY);
      if (cachedData) {
        allSubjects.value = cachedData;
        return;
      }
    }

    try {
      startLoading();

      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("No access token available");

      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/subject`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const subjects = response.data.subjects.map((subject) => ({
        ...subject,
        image: `${import.meta.env.VITE_API_URL}/uploads/subjects/${
          subject.subject_image
        }`,
      }));

      allSubjects.value = subjects;
      console.log("Fetched subjects:", allSubjects.value);
      cache.set(CACHE_KEY, subjects);
    } catch (error) {
      toast.error("Error fetching subjects");
      console.error(
        "Error fetching subjects:",
        error.response?.data || error.message
      );
    } finally {
      stopLoading();
    }
  };

  const invalidateCache = () => {
    cache.clear("subjects_data");
  };

  const updateSubject = (updatedSubject) => {
    const index = allSubjects.value.findIndex(
      (s) => s.id === updatedSubject.id
    );
    if (index !== -1) {
      allSubjects.value[index] = {
        ...updatedSubject,
        image: `${import.meta.env.VITE_API_URL}/uploads/subjects/${
          updatedSubject.subject_image
        }`,
      };
    }
    invalidateCache();
  };

  const deleteSubject = async (subjectId) => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("No access token available");

      const response = await axios.delete(
        `${import.meta.env.VITE_API_URL}/subject/${subjectId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Remove the subject from the local state
      allSubjects.value = allSubjects.value.filter(
        (subject) => subject.id !== subjectId
      );

      // Invalidate cache
      invalidateCache();

      // Show success message
      toast.success(response.data.message);

      return true; // Return true to indicate successful deletion
    } catch (error) {
      console.error("Error deleting subject:", error);
      toast.error(
        error.response?.data?.message || "Error occurred while deleting subject"
      );
      return false; // Return false to indicate failed deletion
    }
  };

  return {
    allSubjects,
    isLoading,
    fetchSubjects,
    invalidateCache,
    updateSubject,
    deleteSubject,
  };
});
