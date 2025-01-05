// utils/cache.js
export const cache = {
  set(key, data, ttl = 5 * 60 * 1000) {
    // 5 minutes default
    localStorage.setItem(
      key,
      JSON.stringify({
        data,
        timestamp: Date.now(),
        ttl,
      })
    );
  },

  get(key) {
    const item = localStorage.getItem(key);
    if (!item) return null;

    const { data, timestamp, ttl } = JSON.parse(item);
    if (Date.now() - timestamp > ttl) {
      localStorage.removeItem(key);
      return null;
    }

    return data;
  },

  clear(key) {
    if (key) {
      localStorage.removeItem(key);
    } else {
      localStorage.clear();
    }
  },
};
