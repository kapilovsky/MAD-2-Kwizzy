// utils/auth.js
export const getUserRole = () => {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role; // or however your role is stored in the token
  } catch (error) {
    console.error("Error parsing token:", error);
    return null;
  }
};

export const getUserId = () => {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub || payload.id; // adjust based on your token structure
  } catch (error) {
    console.error("Error parsing token:", error);
    return null;
  }
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};

export const isAdmin = () => getUserRole() === "admin";
export const isStudent = () => getUserRole() === "student";
