import './assets/main.css'

import { createApp } from 'vue'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import App from './App.vue'
import router from './routers/router'

createApp(App).use(autoAnimatePlugin).use(router).mount('#app')
