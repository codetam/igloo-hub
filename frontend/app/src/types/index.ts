// Base models

export interface Player {
  id: string
  name: string
  nickname?: string
  profile?: string
}

export interface GlobalPlayerStats {
  id: string
  name: string
  nickname?: string
  profile?: string
  games_played: number
  total_goals: number
  total_assists: number
  wins: number
  goals_per_game: number
}

export interface GamePlayerStats {
  game_id: string
  date: string
  stadium: string
  team: 'home' | 'away'
  score: string
  result: 'win' | 'loss' | 'draw'
  goals: number
  assists: number
}

export interface Stadium {
  id: string
  name: string
  address?: string
}

export interface GameScore {
  home_team: number
  away_team: number
}

// Goal with nested player data
export interface Goal {
  id: string
  team_id: string
  minute: string | null
  scorer: Player
  assister: Player | null
}

export interface GamePlayerTeamRead {
  id: string
  name: string
  nickname?: string
  profile?: string
  goals: number
  assists: number
}

export interface GameTeamRead {
  id: string
  name: string | null
  players: GamePlayerTeamRead[]
}

// Request types
export interface PlayerCreate {
  name: string
  nickname?: string
}

export interface GameCreate {
  stadium_id: string
  date: string
}

export interface GoalCreate {
  scorer_id: string
  team_id: string
  assister_id?: string
  minute?: string
}

export interface Game {
  id: string
  date: string
  started_at: string | null
  ended_at: string | null

  stadium?: Stadium | null
  home_team: GameTeamRead
  away_team: GameTeamRead
  goals: Goal[]

  status: 'not_started' | 'started' | 'ended'
  score: GameScore
}