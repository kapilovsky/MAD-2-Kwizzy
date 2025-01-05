// composables/useSubjects.js
import { ref, computed } from "vue";
import axios from "axios";
import { cache } from "@/utils/cache";
import { useToast } from "@/composables/useToast";

export function useSubjects() {
  const allSubjects = ref([]);
  const isLoading = ref(false);
  const loadingTimeout = ref(null);
  const toast = useToast();

  const startLoading = () => {
    // Only show loader if it takes more than 200ms to load
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

  return {
    allSubjects,
    isLoading,
    fetchSubjects,
    invalidateCache,
  };
}
