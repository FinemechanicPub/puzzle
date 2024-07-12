import { createWebHistory, createRouter } from 'vue-router'

// https://router.vuejs.org/guide/advanced/lazy-loading.html
const MainPage = () => import('@/views/MainPage.vue')
const GameView = () => import('@/views/GameView.vue')

const routes = [
  { path: '/', name: 'main', component: MainPage},
  { path: '/game/:id', name: 'game', component: GameView, props: true},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router