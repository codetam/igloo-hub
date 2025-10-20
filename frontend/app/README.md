# 5v5 Football Stats Tracker

A modern, mobile-first web application for tracking 5-a-side football matches, players, and statistics. Built with Vue 3, TypeScript, and Vuetify, with a Champions League-inspired design.

## Features

- 📱 **Mobile-First Design** - Optimized for smartphones with responsive layout
- ⚽ **Match Management** - Create matches, add players to teams, record goals
- 👥 **Player Tracking** - Manage players and view detailed statistics
- 📊 **Statistics** - Track goals, assists, wins, and performance metrics
- 🎨 **Champions League Theme** - Dark blue, bright blue, and gold color scheme
- 🚀 **Modern Stack** - Vue 3 Composition API, TypeScript, Pinia state management

## Tech Stack

- **Frontend Framework**: Vue 3 with Composition API
- **UI Framework**: Vuetify 3 (Material Design)
- **Language**: TypeScript
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **Icons**: Material Design Icons

## Project Structure

```
src/
├── main.ts                 # Application entry point
├── App.vue                 # Root component
├── types/
│   └── index.ts           # TypeScript interfaces
├── router/
│   └── index.ts           # Route configuration
├── stores/
│   ├── players.ts         # Player state management
│   ├── games.ts           # Game state management
│   └── stadiums.ts        # Stadium state management
├── services/
│   └── api.ts             # API service layer
├── plugins/
│   └── vuetify.ts         # Vuetify configuration
├── styles/
│   └── main.css           # Global styles
├── views/
│   ├── HomeView.vue       # Dashboard
│   ├── PlayersView.vue    # Player list
│   ├── PlayerDetailView.vue  # Player details
│   ├── MatchesView.vue    # Match list
│   ├── MatchDetailView.vue   # Match details
│   ├── CreateMatchView.vue   # Create match form
│   └── CreatePlayerView.vue  # Create player form
└── components/
    ├── layout/
    │   ├── AppBar.vue     # Top navigation
    │   └── BottomNav.vue  # Mobile bottom navigation
    ├── match/
    │   ├── MatchCard.vue  # Match summary card
    │   ├── MatchScoreboard.vue  # Score display
    │   ├── TeamLineup.vue  # Team player list
    │   ├── GoalsList.vue   # Goals timeline
    │   └── RecordGoalDialog.vue  # Record goal form
    ├── player/
    │   ├── PlayerCard.vue  # Player card
    │   ├── PlayerStatsCard.vue  # Player statistics
    │   └── PlayerSearchDialog.vue  # Player search
    └── common/
        ├── LoadingSpinner.vue  # Loading indicator
        └── EmptyState.vue      # Empty state placeholder
```

## Setup Instructions

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (FastAPI with SQLModel)

### Installation

1. **Clone or create the project**

```bash
npm create vite@latest 5v5-football-stats -- --template vue-ts
cd 5v5-football-stats
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure API endpoint**

The Vite proxy is configured to forward `/api` requests to `http://localhost:8000`. 

Update `vite.config.ts` if your backend runs on a different port:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:YOUR_PORT',
      changeOrigin: true,
    }
  }
}
```

4. **Start development server**

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Backend Requirements

The frontend expects the following API endpoints:

### Players
- `POST /api/players` - Create player
- `GET /api/players` - List players
- `GET /api/players/{id}` - Get player
- `PUT /api/players/{id}` - Update player
- `DELETE /api/players/{id}` - Delete player
- `GET /api/players/{id}/stats` - Player statistics
- `GET /api/players/{id}/games` - Player match history
- `GET /api/players/search/by-name` - Search players

### Games
- `POST /api/games` - Create game
- `GET /api/games` - List games
- `GET /api/games/{id}` - Get game
- `DELETE /api/games/{id}` - Delete game
- `POST /api/games/{id}/players` - Add player to game
- `POST /api/games/{id}/goals` - Record goal
- `GET /api/games/{id}/score` - Get game score
- `GET /api/games/{id}/players` - Get game players

### Stadiums
- `POST /api/stadiums` - Create stadium
- `GET /api/stadiums` - List stadiums
- `GET /api/stadiums/{id}` - Get stadium
- `PUT /api/stadiums/{id}` - Update stadium
- `DELETE /api/stadiums/{id}` - Delete stadium

## Color Scheme

The application uses a Champions League-inspired color palette:

- **Primary**: `#001E40` (Deep navy blue)
- **Secondary**: `#00B2E3` (Bright blue)
- **Accent**: `#FFD700` (Gold)
- **Background**: `#0A1628` (Very dark blue)
- **Surface**: `#1A2942` (Dark blue surface)

## Key Features

### Home Dashboard
- Quick actions for creating matches and players
- Recent matches list
- Player grid preview

### Match Management
- Create matches with stadium and date
- Add players to Team 1 and Team 2
- Record goals with scorer, assister, and minute
- View match details and score
- Timeline of goals

### Player Statistics
- Total goals and assists
- Games played and wins
- Goals per game ratio
- Win rate percentage
- Match history with results

### Mobile Experience
- Bottom navigation bar
- Responsive cards and layouts
- Touch-friendly interactions
- Optimized for small screens

## Development

### Type Safety
All components use TypeScript for full type safety. Types are defined in `src/types/index.ts`.

### State Management
Pinia stores handle all state:
- `usePlayersStore()` - Player data
- `useGamesStore()` - Match data
- `useStadiumsStore()` - Stadium data

### API Service
All API calls are centralized in `src/services/api.ts` using Axios.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!