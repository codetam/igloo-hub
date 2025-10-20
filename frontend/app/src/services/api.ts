import axios from 'axios'
import type {
  Player,
  Stadium,
  GameListItem,
  GameDetail,
  PlayerStats,
  PlayerGame,
  GameScore,
  TeamPlayers,
  CreatePlayerRequest,
  CreateGameRequest,
  AddPlayerToGameRequest,
  RecordGoalRequest,
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Players
export const playersApi = {
  create: (data: CreatePlayerRequest) => api.post<Player>('/players', null, { params: data }),
  getById: (id: string) => api.get<Player>(`/players/${id}`),
  list: (skip = 0, limit = 50) => api.get<Player[]>('/players', { params: { skip, limit } }),
  update: (id: string, data: Partial<CreatePlayerRequest>) => api.put<Player>(`/players/${id}`, null, { params: data }),
  delete: (id: string) => api.delete(`/players/${id}`),
  getStats: (id: string) => api.get<PlayerStats>(`/players/${id}/stats`),
  getGames: (id: string) => api.get<PlayerGame[]>(`/players/${id}/games`),
  searchByName: (name: string) => api.get<Player[]>('/players/search/by-name', { params: { name } }),
}

// Games
export const gamesApi = {
  create: (data: CreateGameRequest) => api.post<GameListItem>('/games', null, { params: data }),
  getById: (id: string) => api.get<GameDetail>(`/games/${id}`),
  list: (skip = 0, limit = 20) => api.get<GameListItem[]>('/games', { params: { skip, limit } }),
  delete: (id: string) => api.delete(`/games/${id}`),
  addPlayer: (gameId: string, data: AddPlayerToGameRequest) => 
    api.post(`/games/${gameId}/players`, null, { params: data }),
  recordGoal: (gameId: string, data: RecordGoalRequest) => 
    api.post(`/games/${gameId}/goals`, null, { params: data }),
  getScore: (gameId: string) => api.get<GameScore>(`/games/${gameId}/score`),
  getPlayers: (gameId: string) => api.get<TeamPlayers>(`/games/${gameId}/players`),
}

// Stadiums
export const stadiumsApi = {
  create: (name: string, address?: string) => 
    api.post<Stadium>('/stadiums', null, { params: { name, address } }),
  getById: (id: string) => api.get<Stadium>(`/stadiums/${id}`),
  list: (skip = 0, limit = 50) => api.get<Stadium[]>('/stadiums', { params: { skip, limit } }),
  update: (id: string, name?: string, address?: string) => 
    api.put<Stadium>(`/stadiums/${id}`, null, { params: { name, address } }),
  delete: (id: string) => api.delete(`/stadiums/${id}`),
}

export default api