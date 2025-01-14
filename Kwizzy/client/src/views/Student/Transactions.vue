<template>
  <Loader v-if="isLoading" />
  <div v-else>
    <div class="absolute sm:top-6 top-16">
      <div class="sm:w-[450px] w-[300px]">
        <SearchBar
          @search="handleSearch"
          placeholder="Search quiz name, amount or transaction id..."
        />
      </div>
    </div>

    <div class="sm:mt-4 mt-16">
      <h1 class="sm:text-5xl text-3xl font-bold tracking-tighter">
        Transactions
      </h1>

      <div>
        <table class="w-full table-auto mt-8">
          <thead>
            <tr class="bg-gray-200 text-left p-1 border-b-2 border-black">
              <th>S.No</th>
              <th>Transaction ID</th>
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
              <td>{{ transaction.quiz }}</td>
              <td>{{ transaction.amount }}</td>
              <td class="text-right">{{ transaction.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import SearchBar from "@/components/Admin/SearchBar.vue";

const API_URL = import.meta.env.VITE_API_URL;
const isLoading = ref(true);
const route = useRoute();
const studentId = route.params.id;
const transactions = ref([]);
const searchQuery = ref("");

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
});

const handleSearch = (query) => {
  searchQuery.value = query;
};

const filteredTransactions = computed(() => {
  if (!searchQuery.value) return transactions.value;

  //search by quiz name or amount or transaction id

  return transactions.value.filter(
    (transaction) =>
      transaction.quiz
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      transaction.amount.toString().includes(searchQuery.value) ||
      transaction.transaction_id
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
  );
});

const fetchTransactions = async () => {
  try {
    isLoading.value = true;
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Token not found");

    const response = await axios.get(
      `${API_URL}/payments/history/${studentId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
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
