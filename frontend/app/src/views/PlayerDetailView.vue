<template>
  <v-container class="py-6">
    <LoadingSpinner v-if="loading" message="Caricamento..." />

    <div v-else-if="player">
      <!-- Player Header -->
      <v-card class="mb-6 cl-gradient" elevation="4">
        <v-card-text class="pa-6 text-center">
          <v-avatar size="100" color="secondary" class="mb-4">
            <v-icon size="60">mdi-account</v-icon>
          </v-avatar>
          <h1 class="text-h4 font-weight-bold">{{ player.name }}</h1>
          <p v-if="player.nickname" class="text-h6 text-secondary mt-2">
            "{{ player.nickname }}"
          </p>
        </v-card-text>
      </v-card>

      <!-- Stats Cards -->
      <v-row v-if="player" class="mb-6">
        <v-col cols="6" sm="3">
          <v-card elevation="2">
            <v-card-text class="text-center pa-4">
              <v-icon size="40" color="secondary" class="mb-2">mdi-soccer</v-icon>
              <div class="text-h4 font-weight-bold gold-text">{{ player.total_goals }}</div>
              <div class="text-caption">Goal</div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="6" sm="3">
          <v-card elevation="2">
            <v-card-text class="text-center pa-4">
              <v-icon size="40" color="accent" class="mb-2">mdi-hand-pointing-right</v-icon>
              <div class="text-h4 font-weight-bold gold-text">{{ player.total_assists }}</div>
              <div class="text-caption">Assist</div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="6" sm="3">
          <v-card elevation="2">
            <v-card-text class="text-center pa-4">
              <v-icon size="40" color="success" class="mb-2">mdi-trophy</v-icon>
              <div class="text-h4 font-weight-bold gold-text">{{ player.wins }}</div>
              <div class="text-caption">Vittorie</div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="6" sm="3">
          <v-card elevation="2">
            <v-card-text class="text-center pa-4">
              <v-icon size="40" color="info" class="mb-2">mdi-soccer-field</v-icon>
              <div class="text-h4 font-weight-bold gold-text">{{ player.games_played }}</div>
              <div class="text-caption">Partite</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Additional Stats -->
      <v-card v-if="player" class="mb-6" elevation="2">
        <v-card-text class="pa-4">
          <v-row>
            <v-col cols="12" sm="6">
              <div class="stat-item">
                <span class="text-body-2 text-secondary">Goal per Partita</span>
                <span class="text-h6 font-weight-bold ml-auto">{{ player.goals_per_game }}</span>
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="stat-item">
                <span class="text-body-2 text-secondary">Win Rate</span>
                <span class="text-h6 font-weight-bold ml-auto">
                  {{ winRate }}%
                </span>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Match History -->
      <div>
        <h2 class="text-h5 mb-4 ml-2">Partite Giocate</h2>

        <LoadingSpinner v-if="loadingGames" message="Loading games..." />

        <EmptyState v-else-if="playerGames.length === 0" icon="mdi-soccer-field" title="Non ci sono partite"
          message="Il giocatore non ha ancora giocato una partita" />

        <v-card v-else v-for="game in playerGames" :key="game.game_id"
          :to="{ name: 'match-detail', params: { id: game.game_id } }" class="mb-3" elevation="2" hover>
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-chip :color="game.result === 'win' ? 'success' : game.result === 'loss' ? 'error' : 'warning'"
                size="small" class="mr-2">
                {{ game.result.toUpperCase() }}
              </v-chip>
              <v-chip size="small" variant="outlined" class="mr-2">
                Team {{ game.team }}
              </v-chip>
              <v-spacer></v-spacer>
              <span class="text-caption">{{ formatDate(game.date) }}</span>
            </div>

            <div class="d-flex align-center">
              <v-icon size="20" class="mr-2">mdi-map-marker</v-icon>
              <span class="text-body-2">{{ game.stadium }}</span>
              <v-spacer></v-spacer>
              <span class="text-h6 font-weight-bold">{{ game.score }}</span>
            </div>

            <div v-if="game.goals > 0 || game.assists > 0" class="mt-2 d-flex gap-3">
              <v-chip v-if="game.goals > 0" size="small" color="secondary">
                <v-icon start size="16">mdi-soccer</v-icon>
                {{ game.goals }} goal{{ game.goals > 1 ? 's' : '' }}
              </v-chip>
              <v-chip v-if="game.assists > 0" size="small" color="accent">
                <v-icon start size="16">mdi-hand-pointing-right</v-icon>
                {{ game.assists }} assist{{ game.assists > 1 ? 's' : '' }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </div>
    </div>

    <EmptyState v-else icon="mdi-account-off" title="Giocatore non trovato"
      message="Il giocatore che cerchi non esiste" />
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePlayersStore } from '@/stores/players'
import { formatDate as formatDateUtil } from '@/utils/dateUtils'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const playersStore = usePlayersStore()

const loading = ref(false)
const loadingGames = ref(false)

const player = computed(() => playersStore.currentPlayer)
const playerGames = computed(() => playersStore.currentPlayerGames)

const winRate = computed(() => {
  if (!player.value || player.value.games_played === 0) return 0
  return Math.round((player.value.wins / player.value.games_played) * 100)
})

function formatDate(dateString: string) {
  return formatDateUtil(dateString)
}

onMounted(async () => {
  const playerId = route.params.id as string

  loading.value = true
  await Promise.all([
    playersStore.fetchPlayerById(playerId)
  ])
  loading.value = false

  loadingGames.value = true
  await playersStore.fetchPlayerGames(playerId)
  loadingGames.value = false
})
</script>

<style scoped>
.stat-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: rgba(26, 41, 66, 0.5);
  border-radius: 8px;
}
</style>