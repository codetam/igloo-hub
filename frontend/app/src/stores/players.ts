import { defineStore } from 'pinia'
import { ref } from 'vue'
import { playersApi } from '@/services/api'
import type { Player, PlayerStats, PlayerGame, CreatePlayerRequest } from '@/types'

export const usePlayersStore = defineStore('players', () => {
  const players = ref<Player[]>([])
  const currentPlayer = ref<Player | null>(null)
  const currentPlayerStats = ref<PlayerStats | null>(null)
  const currentPlayerGames = ref<PlayerGame[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchPlayers() {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.list()
      players.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch players'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchPlayerById(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.getById(id)
      currentPlayer.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch player'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchPlayerStats(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.getStats(id)
      currentPlayerStats.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch player stats'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchPlayerGames(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.getGames(id)
      currentPlayerGames.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch player games'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function createPlayer(data: CreatePlayerRequest) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.create(data)
      players.value.push(response.data)
      return response.data
    } catch (e) {
      error.value = 'Failed to create player'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updatePlayer(id: string, data: Partial<CreatePlayerRequest>) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.update(id, data)
      const index = players.value.findIndex(p => p.id === id)
      if (index !== -1) {
        players.value[index] = response.data
      }
      if (currentPlayer.value?.id === id) {
        currentPlayer.value = response.data
      }
      return response.data
    } catch (e) {
      error.value = 'Failed to update player'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deletePlayer(id: string) {
    loading.value = true
    error.value = null
    try {
      await playersApi.delete(id)
      players.value = players.value.filter(p => p.id !== id)
    } catch (e) {
      error.value = 'Failed to delete player'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function searchPlayers(name: string) {
    loading.value = true
    error.value = null
    try {
      const response = await playersApi.searchByName(name)
      return response.data
    } catch (e) {
      error.value = 'Failed to search players'
      console.error(e)
      return []
    } finally {
      loading.value = false
    }
  }

  return {
    players,
    currentPlayer,
    currentPlayerStats,
    currentPlayerGames,
    loading,
    error,
    fetchPlayers,
    fetchPlayerById,
    fetchPlayerStats,
    fetchPlayerGames,
    createPlayer,
    updatePlayer,
    deletePlayer,
    searchPlayers,
  }
})