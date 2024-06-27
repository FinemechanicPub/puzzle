import { createWebHistory, createRouter } from 'vue-router'

import GameView from '../views/GameView.vue'

const routes = [
  { path: '/game/:id', component: GameView, props: true},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router