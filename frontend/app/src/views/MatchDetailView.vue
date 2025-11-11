<template>
  <v-container class="py-6">
    <LoadingSpinner v-if="loading" message="Caricamento..." />

    <div v-else-if="game">
      <!-- Match Header -->
      <v-card class="mb-6" elevation="4">
        <v-card-text class="pa-6">

          <!-- Date and Stadium -->
          <div class="d-flex align-center mb-4">
            <div>
              <v-chip prepend-icon="mdi-calendar" color="secondary">
                {{ formattedDate }}
              </v-chip>
              <v-chip prepend-icon="mdi-map-marker" color="surface-variant" class="ml-2">
                {{ game.stadium.name }}
              </v-chip>
              <v-chip v-if="gameStatus === 'live'" color="error" text-color="white" prepend-icon="mdi-record-circle"
                class="ml-2">
                LIVE
              </v-chip>

              <v-chip v-else-if="gameStatus === 'ended'" color="grey" prepend-icon="mdi-stop-circle" class="ml-2">
                Terminato
              </v-chip>

              <v-chip v-else color="blue-grey" prepend-icon="mdi-clock-outline" class="ml-2">
                Inizia tra poco
              </v-chip>
            </div>

            <v-spacer></v-spacer>
            <v-btn v-if="gameStatus === 'not_started'" color="success" prepend-icon="mdi-play-circle"
              @click="startMatch" :loading="actionLoading">
              Start
            </v-btn>

            <v-btn v-else-if="gameStatus === 'live'" color="error" prepend-icon="mdi-stop-circle" @click="endMatch"
              :loading="actionLoading">
              Stop
            </v-btn>
          </div>

          <!-- Scoreboard -->
          <MatchScoreboard v-if="score" :score="score" />

          <!-- Notes -->
          <v-alert v-if="game.notes" type="info" variant="tonal" class="mt-4">
            <v-icon start>mdi-note-text</v-icon>
            {{ game.notes }}
          </v-alert>
        </v-card-text>
      </v-card>

      <!-- Record Goal Button -->
      <v-btn block size="large" color="accent" prepend-icon="mdi-soccer" @click="showRecordGoal = true" class="mb-6">
        Aggiungi Goal
      </v-btn>

      <!-- Teams -->
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <TeamLineup :team-number="1" :players="teamPlayers?.team_1 || []" @add-player="openAddPlayerDialog(1)" />
        </v-col>
        <v-col cols="12" md="6">
          <TeamLineup :team-number="2" :players="teamPlayers?.team_2 || []" @add-player="openAddPlayerDialog(2)" />
        </v-col>
      </v-row>

      <!-- Match Timeline -->
      <MatchTimeline v-if="game.started_at" :goals="game.goals" :start-time="game.started_at" :end-time="game.ended_at"
        :is-live="gameStatus === 'live'" class="mb-6" />

      <!-- Goals Timeline -->
      <GoalsList v-if="game.goals && game.goals.length > 0" :goals="game.goals" :game-start-time="game.date" />

      <!-- Delete Match -->
      <v-card class="mt-6" elevation="0" color="transparent">
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="outlined" prepend-icon="mdi-delete" @click="showDeleteDialog = true">
            Elimina Partita
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>

    <EmptyState v-else icon="mdi-soccer-field" title="Partita non trovata"
      message="La partita che stai cercando non esiste" />

    <!-- Record Goal Dialog -->
    <RecordGoalDialog v-model="showRecordGoal" :game-id="game?.id || ''" :team-players="teamPlayers"
      @goal-recorded="refreshMatchData" />

    <!-- Add Player Dialog -->
    <v-dialog v-model="showAddPlayer" max-width="600">
      <v-card>
        <v-card-title>
          Add Player to Team {{ selectedTeam }}
        </v-card-title>
        <v-card-text>
          <PlayerSearchDialog v-model="showAddPlayer" :exclude-ids="allPlayerIds" @select="handleAddPlayer" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6">Elimina Partita?</v-card-title>
        <v-card-text>
          Sicuro di voler eliminare la partita? L'eliminazione non può essere annullata.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showDeleteDialog = false">Annulla</v-btn>
          <v-btn color="error" @click="deleteMatch" :loading="deleting">Elimina</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import { formatDateTime } from '@/utils/dateUtils'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import MatchScoreboard from '@/components/match/MatchScoreboard.vue'
import TeamLineup from '@/components/match/TeamLineup.vue'
import GoalsList from '@/components/match/GoalsList.vue'
import RecordGoalDialog from '@/components/match/RecordGoalDialog.vue'
import PlayerSearchDialog from '@/components/player/PlayerSearchDialog.vue'

const route = useRoute()
const router = useRouter()
const gamesStore = useGamesStore()

const loading = ref(false)
const showRecordGoal = ref(false)
const showAddPlayer = ref(false)
const showDeleteDialog = ref(false)
const deleting = ref(false)
const selectedTeam = ref<1 | 2>(1)

const game = computed(() => gamesStore.currentGame)
const score = computed(() => gamesStore.currentGameScore)
const teamPlayers = computed(() => gamesStore.currentGamePlayers)

const formattedDate = computed(() => {
  if (!game.value) return ''
  return formatDateTime(game.value.date)
})

const allPlayerIds = computed(() => {
  if (!teamPlayers.value) return []
  return [
    ...teamPlayers.value.team_1.map(p => p.id),
    ...teamPlayers.value.team_2.map(p => p.id)
  ]
})

const actionLoading = ref(false)

const gameStatus = computed<'not_started' | 'live' | 'ended'>(() => {
  if (!game.value) return 'not_started'
  if (game.value.ended_at) return 'ended'
  if (game.value.started_at) return 'live'
  return 'not_started'
})

async function startMatch() {
  if (!game.value) return
  actionLoading.value = true
  try {
    await gamesStore.startGame(game.value.id)
    await refreshMatchData()
  } catch (e) {
    console.error('Cannot start game:', e)
  } finally {
    actionLoading.value = false
  }
}

async function endMatch() {
  if (!game.value) return
  actionLoading.value = true
  try {
    await gamesStore.endGame(game.value.id)
    await refreshMatchData()
  } catch (e) {
    console.error('Cannot end game:', e)
  } finally {
    actionLoading.value = false
  }
}


function openAddPlayerDialog(team: 1 | 2) {
  selectedTeam.value = team
  showAddPlayer.value = true
}

async function handleAddPlayer(player: any) {
  if (!game.value) return

  try {
    await gamesStore.addPlayerToGame(game.value.id, {
      player_id: player.id,
      team: selectedTeam.value
    })
    showAddPlayer.value = false
  } catch (e) {
    console.error('Giocatore non può essere aggiunto:', e)
  }
}

async function refreshMatchData() {
  if (!game.value) return

  await Promise.all([
    gamesStore.fetchGameById(game.value.id),
    gamesStore.fetchGameScore(game.value.id),
    gamesStore.fetchGamePlayers(game.value.id)
  ])
}

async function deleteMatch() {
  if (!game.value) return

  deleting.value = true
  try {
    await gamesStore.deleteGame(game.value.id)
    router.push({ name: 'matches' })
  } catch (e) {
    console.error('La Partita non può essere eliminata:', e)
  } finally {
    deleting.value = false
    showDeleteDialog.value = false
  }
}

onMounted(async () => {
  const gameId = route.params.id as string

  loading.value = true
  await Promise.all([
    gamesStore.fetchGameById(gameId),
    gamesStore.fetchGameScore(gameId),
    gamesStore.fetchGamePlayers(gameId)
  ])
  loading.value = false
})
</script>

<style scoped>
/* Additional styles if needed */
</style>