// src/services/studentService.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const studentService = {
  // Get all students with pagination, search, and sorting
  async getStudents(params = {}) {
    const {
      page = 1,
      per_page = 10,
      search = "",
      sort_by = "name",
      order = "asc",
    } = params;

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Token not found");
      }
      const response = await axios.get(`${API_URL}/students`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          page,
          per_page,
          search,
          sort_by,
          order,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching students:", error);
      throw error;
    }
  },

  // Get specific student
  async getStudent(id) {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${API_URL}/student/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching student:", error);
      throw error;
    }
  },

  // Get student statistics
  async getStatistics() {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${API_URL}/student/statistics`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching statistics:", error);
      throw error;
    }
  },
};
