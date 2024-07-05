import { createWebHistory, createRouter } from 'vue-router'

import MainPage from '@/views/MainPage.vue'
import GameView from '@/views/GameView.vue'

const routes = [
  { path: '/', name: 'main', component: MainPage},
  { path: '/game/:id', name: 'game', component: GameView, props: true},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router