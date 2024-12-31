import "./assets/input.css";
import "./assets/output.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { VueScrollTo } from "vue-scrollto";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(VueScrollTo);
app.use(router);

app.mount("#app");
