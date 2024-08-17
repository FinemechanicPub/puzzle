import './assets/main.css'

import { createApp } from 'vue'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { OpenAPI } from  './api/generated/core/OpenAPI';
import Vue3Tour from 'vue3-tour';

import App from './App.vue';
import router from './routers/router';

if (import.meta.env.DEV){
    console.log(`base api url: ${import.meta.env.VITE_API_BASE_URI}`)
    OpenAPI.BASE = `${import.meta.env.VITE_API_BASE_URI}`
}
createApp(App).use(autoAnimatePlugin).use(router).use(Vue3Tour).mount('#app')
