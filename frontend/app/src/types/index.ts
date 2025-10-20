// Base models
export interface Stadium {
  id: string
  name: string
  address?: string
}

export interface Player {
  id: string
  name: string
  nickname?: string
  profile?: string
}

// Goal with nested player data
export interface Goal {
  id: string
  team: number
  minute?: string // Now a datetime string
  scorer: Player
  assister?: Player | null
}

// Game list response (minimal data)
export interface GameListItem {
  id: string
  date: string
  stadium_id: string
  notes?: string
}

// Game detail response (full data with nested objects)
export interface GameDetail {
  id: string
  date: string
  notes?: string
  stadium: Stadium
  goals: Goal[]
}

// Player in game context (with stats)
export interface PlayerInGame {
  id: string
  name: string
  nickname?: string
  goals: number
  assists: number
}

// Team players response
export interface TeamPlayers {
  team_1: PlayerInGame[]
  team_2: PlayerInGame[]
}

// Game score response
export interface GameScore {
  game_id: string
  team_1: number
  team_2: number
  winner?: number | null
  status: string
}

// Player statistics
export interface PlayerStats {
  player_id: string
  name: string
  nickname?: string
  games_played: number
  total_goals: number
  total_assists: number
  wins: number
  goals_per_game: number
}

// Player game history item
export interface PlayerGame {
  game_id: string
  date: string
  stadium: string
  team: number
  score: string
  result: 'win' | 'draw' | 'loss'
  goals: number
  assists: number
}

// Request types
export interface CreatePlayerRequest {
  name: string
  nickname?: string
}

export interface CreateGameRequest {
  stadium_id: string
  date: string
  notes?: string
}

export interface AddPlayerToGameRequest {
  player_id: string
  team: number
}

export interface RecordGoalRequest {
  scorer_id: string
  team: number
  assister_id?: string
  minute?: string
}