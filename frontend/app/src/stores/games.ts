import { defineStore } from 'pinia'
import { ref } from 'vue'
import { gamesApi } from '@/services/api'
import type { Game, GameCreate, GoalCreate } from '@/types'

export const useGamesStore = defineStore('games', () => {
  const games = ref<Game[]>([])
  const currentGame = ref<Game | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchGames() {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.list()
      games.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch games'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchGameById(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.getById(id)
      currentGame.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch game'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function createGame(data: GameCreate) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.create(data)
      games.value.unshift(response.data)
      return response.data
    } catch (e) {
      error.value = 'Failed to create game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function addPlayerToGame(gameId: string, playerId: string, teamId: string) {
    loading.value = true
    error.value = null
    try {
      await gamesApi.addPlayer(gameId, playerId, teamId)
      // Refresh game to get updated player list
      await fetchGameById(gameId)
    } catch (e) {
      error.value = 'Failed to add player to game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function recordGoal(gameId: string, data: GoalCreate) {
    loading.value = true
    error.value = null
    try {
      await gamesApi.recordGoal(gameId, data)
      // Refresh game to get updated score and goals
      await fetchGameById(gameId)
    } catch (e) {
      error.value = 'Failed to record goal'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteGame(id: string) {
    loading.value = true
    error.value = null
    try {
      await gamesApi.delete(id)
      games.value = games.value.filter(g => g.id !== id)
    } catch (e) {
      error.value = 'Failed to delete game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function startGame(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.startGame(id)
      currentGame.value = response.data
      // Update in the list as well
      const index = games.value.findIndex(g => g.id === id)
      if (index !== -1) {
        games.value[index] = response.data
      }
    } catch (e) {
      error.value = 'Failed to start game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function endGame(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.endGame(id)
      currentGame.value = response.data
      // Update in the list as well
      const index = games.value.findIndex(g => g.id === id)
      if (index !== -1) {
        games.value[index] = response.data
      }
    } catch (e) {
      error.value = 'Failed to end game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    games,
    currentGame,
    loading,
    error,
    fetchGames,
    fetchGameById,
    createGame,
    addPlayerToGame,
    recordGoal,
    deleteGame,
    startGame,
    endGame,
  }
})