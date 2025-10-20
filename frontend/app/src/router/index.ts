import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/players',
      name: 'players',
      component: () => import('@/views/PlayersView.vue'),
    },
    {
      path: '/players/create',
      name: 'create-player',
      component: () => import('@/views/CreatePlayerView.vue'),
    },
    {
      path: '/players/:id',
      name: 'player-detail',
      component: () => import('@/views/PlayerDetailView.vue'),
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('@/views/MatchesView.vue'),
    },
    {
      path: '/matches/create',
      name: 'create-match',
      component: () => import('@/views/CreateMatchView.vue'),
    },
    {
      path: '/matches/:id',
      name: 'match-detail',
      component: () => import('@/views/MatchDetailView.vue'),
    },
  ],
})

export default router