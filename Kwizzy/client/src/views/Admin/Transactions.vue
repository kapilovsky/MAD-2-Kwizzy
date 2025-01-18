<template>
  <Loader v-if="isLoading" />
  <Sidebar v-else>
    <div>
      <header class="h-16 bg-white flex items-center justify-between gap-6">
        <div class="flex items-center flex-1">
          <div class="flex-1 max-w-lg">
            <div class="relative">
              <SearchBar
                @search="handleSearch"
                placeholder="Search quiz name, user name, or transaction ID..."
              />
            </div>
          </div>
        </div>

        <!-- Right Side Icons -->
        <div class="flex items-center">
          <div class="flex items-center gap-4">
            <img
              :src="logo"
              alt="User avatar"
              class="w-8 h-8 rounded-full mix-blend-difference"
            />
            <span class="text-sm font-medium text-gray-700">Admin</span>
          </div>
        </div>
      </header>

      <div class="sm:mt-4 mt-16">
        <div class="flex items-center justify-between">
          <h1 class="sm:text-5xl text-3xl font-bold tracking-tighter">
            Transactions
          </h1>
          <button
            @click="exportTransactions"
            class="text-[#192227] font-bold sohne tracking-tighter"
            :disabled="isExporting"
          >
            <span>{{ isExporting ? "Exporting..." : "[Export CSV]" }}</span>
          </button>
        </div>

        <div>
          <table class="w-full table-auto mt-8">
            <thead>
              <tr class="bg-gray-200 text-left p-1 border-b-2 border-black">
                <th>S.No</th>
                <th>Transaction ID</th>
                <th>User</th>
                <th>Quiz Name</th>
                <th>Amount</th>
                <th class="text-right">Payment Date</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(transaction, index) in filteredTransactions"
                :key="transaction.id"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ transaction.transaction_id }}</td>
                <td>{{ transaction.user }}</td>
                <td>{{ transaction.quiz }}</td>
                <td>{{ transaction.amount }}</td>
                <td class="text-right">{{ transaction.created_at }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div></Sidebar
  >
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";
import Sidebar from "@/components/Admin/Sidebar.vue";
import logo from "../../assets/images/landing-page/white logo.png";

const API_URL = import.meta.env.VITE_API_URL;
const isLoading = ref(true);
const route = useRoute();
const transactions = ref([]);
const searchQuery = ref("");
const isExporting = ref(false);

const handleSearch = (query) => {
  searchQuery.value = query;
};

const filteredTransactions = computed(() => {
  if (!searchQuery.value) return transactions.value;

  return transactions.value.filter(
    (transaction) =>
      transaction.quiz
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      transaction.user
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      transaction.transaction_id
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
  );
});

const exportTransactions = async () => {
  try {
    isExporting.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Token not found");

    const response = await axios.get(`${API_URL}/export/transactions`, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute(
      "download",
      `transactions_${new Date().toISOString().split("T")[0]}.csv`
    );
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error exporting transactions:", error);
  } finally {
    isExporting.value = false;
  }
};

const fetchTransactions = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Token not found");

    const response = await axios.get(`${API_URL}/payments/history`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    transactions.value = response.data.payments;
    console.log("API Response:", response.data);
  } catch (error) {
    console.error("Error fetching transactions:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchTransactions();
});
</script>

<style scoped>
tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

table {
  border-collapse: collapse;
}
</style>
