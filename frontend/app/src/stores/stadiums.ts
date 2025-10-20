import { defineStore } from 'pinia'
import { ref } from 'vue'
import { stadiumsApi } from '@/services/api'
import type { Stadium } from '@/types'

export const useStadiumsStore = defineStore('stadiums', () => {
  const stadiums = ref<Stadium[]>([])
  const currentStadium = ref<Stadium | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchStadiums() {
    loading.value = true
    error.value = null
    try {
      const response = await stadiumsApi.list()
      stadiums.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch stadiums'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchStadiumById(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await stadiumsApi.getById(id)
      currentStadium.value = response.data
    } catch (e) {
      error.value = 'Failed to fetch stadium'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function createStadium(name: string, address?: string) {
    loading.value = true
    error.value = null
    try {
      const response = await stadiumsApi.create(name, address)
      stadiums.value.push(response.data)
      return response.data
    } catch (e) {
      error.value = 'Failed to create stadium'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateStadium(id: string, name?: string, address?: string) {
    loading.value = true
    error.value = null
    try {
      const response = await stadiumsApi.update(id, name, address)
      const index = stadiums.value.findIndex(s => s.id === id)
      if (index !== -1) {
        stadiums.value[index] = response.data
      }
      if (currentStadium.value?.id === id) {
        currentStadium.value = response.data
      }
      return response.data
    } catch (e) {
      error.value = 'Failed to update stadium'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteStadium(id: string) {
    loading.value = true
    error.value = null
    try {
      await stadiumsApi.delete(id)
      stadiums.value = stadiums.value.filter(s => s.id !== id)
    } catch (e) {
      error.value = 'Failed to delete stadium'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    stadiums,
    currentStadium,
    loading,
    error,
    fetchStadiums,
    fetchStadiumById,
    createStadium,
    updateStadium,
    deleteStadium,
  }
})