import axios from 'axios'
import type {
  Player,
  Stadium,
  Game,
  GlobalPlayerStats,
  GamePlayerStats,
  PlayerCreate,
  GameCreate,
  GoalCreate,
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Players
export const playersApi = {
  create: (data: PlayerCreate) => api.post<Player>('/players', data),
  getById: (id: string) => api.get<GlobalPlayerStats>(`/players/${id}`),
  list: (skip = 0, limit = 50) => api.get<GlobalPlayerStats[]>('/players', { params: { skip, limit } }),
  update: (id: string, data: PlayerCreate) => api.put<GlobalPlayerStats>(`/players/${id}`, data),
  delete: (id: string) => api.delete(`/players/${id}`),
  getGames: (id: string) => api.get<GamePlayerStats[]>(`/players/${id}/games`),
  searchByName: (name: string) => api.get<Player[]>('/players/search/by-name', { params: { name } }),
}

// Games
export const gamesApi = {
  create: (data: GameCreate) => api.post<Game>('/games', data),
  getById: (id: string) => api.get<Game>(`/games/${id}`),
  list: (skip = 0, limit = 20) => api.get<Game[]>('/games', { params: { skip, limit } }),
  delete: (id: string) => api.delete(`/games/${id}`),
  addPlayer: (gameId: string, playerId: string, teamId: string) => 
    api.post(`/games/${gameId}/players`, { player_id: playerId, team_id: teamId }),
  recordGoal: (gameId: string, data: GoalCreate) => 
    api.post(`/games/${gameId}/goals`, data),
  startGame: (gameId: string) => api.put<Game>(`/games/${gameId}/start`),
  endGame: (gameId: string) => api.put<Game>(`/games/${gameId}/end`),
}

// Stadiums
export const stadiumsApi = {
  create: (data: { name: string; address?: string }) => 
    api.post<Stadium>('/stadiums', data),
  getById: (id: string) => api.get<Stadium>(`/stadiums/${id}`),
  list: (skip = 0, limit = 50) => api.get<Stadium[]>('/stadiums', { params: { skip, limit } }),
  update: (id: string, name?: string, address?: string) => 
    api.put<Stadium>(`/stadiums/${id}`, undefined, { params: { name, address } }),
  delete: (id: string) => api.delete(`/stadiums/${id}`),
}

export default api