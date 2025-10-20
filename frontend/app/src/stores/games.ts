import { defineStore } from 'pinia'
import { ref } from 'vue'
import { gamesApi } from '@/services/api'
import type {
  GameListItem,
  GameDetail,
  GameScore,
  TeamPlayers,
  CreateGameRequest,
  AddPlayerToGameRequest,
  RecordGoalRequest,
} from '@/types'

export const useGamesStore = defineStore('games', () => {
  const games = ref<GameListItem[]>([])
  const currentGame = ref<GameDetail | null>(null)
  const currentGameScore = ref<GameScore | null>(null)
  const currentGamePlayers = ref<TeamPlayers | null>(null)
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

  async function fetchGameScore(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.getScore(id)
      currentGameScore.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch game score'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchGamePlayers(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await gamesApi.getPlayers(id)
      currentGamePlayers.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch game players'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function createGame(data: CreateGameRequest) {
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

  async function addPlayerToGame(gameId: string, data: AddPlayerToGameRequest) {
    loading.value = true
    error.value = null
    try {
      await gamesApi.addPlayer(gameId, data)
      // Refresh game players
      await fetchGamePlayers(gameId)
    } catch (e) {
      error.value = 'Failed to add player to game'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function recordGoal(gameId: string, data: RecordGoalRequest) {
    loading.value = true
    error.value = null
    try {
      await gamesApi.recordGoal(gameId, data)
      // Refresh game data
      await Promise.all([
        fetchGameScore(gameId),
        fetchGamePlayers(gameId),
        fetchGameById(gameId),
      ])
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

  return {
    games,
    currentGame,
    currentGameScore,
    currentGamePlayers,
    loading,
    error,
    fetchGames,
    fetchGameById,
    fetchGameScore,
    fetchGamePlayers,
    createGame,
    addPlayerToGame,
    recordGoal,
    deleteGame,
  }
})