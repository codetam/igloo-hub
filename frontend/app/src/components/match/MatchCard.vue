<template>
  <v-card
    :to="{ name: 'match-detail', params: { id: game.id } }"
    class="match-card"
    elevation="2"
    hover
  >
    <v-card-text class="pa-4">
      <!-- Date and Stadium -->
      <div class="d-flex align-center mb-3">
        <v-icon size="20" class="mr-2 text-secondary">mdi-calendar</v-icon>
        <span class="text-caption">{{ formattedDate }}</span>
        <v-spacer></v-spacer>
        <v-chip size="small" color="surface-variant">
          <v-icon start size="16">mdi-map-marker</v-icon>
          Stadio
        </v-chip>
      </div>

      <!-- Score Display -->
      <div class="score-section">
        <div class="team-score">
          <div class="text-h5 font-weight-bold">{{ score.team_1 }}</div>
          <div class="text-caption text-secondary">Team 1</div>
        </div>

        <div class="vs-divider">
          <v-icon size="24" color="accent">mdi-sword-cross</v-icon>
        </div>

        <div class="team-score">
          <div class="text-h5 font-weight-bold">{{ score.team_2 }}</div>
          <div class="text-caption text-secondary">Team 2</div>
        </div>
      </div>

      <!-- Winner Badge -->
      <div v-if="winner" class="text-center mt-3">
        <v-chip
          :color="winner === 1 ? 'secondary' : 'accent'"
          size="small"
          prepend-icon="mdi-trophy"
        >
          Team {{ winner }} Vince
        </v-chip>
      </div>

      <!-- Draw -->
      <div v-else-if="score.team_1 === score.team_2 && (score.team_1 > 0 || score.team_2 > 0)" class="text-center mt-3">
        <v-chip size="small" color="warning">
          Pareggio
        </v-chip>
      </div>

      <!-- Notes -->
      <div v-if="score.status" class="mt-3">
        <v-icon size="16" class="mr-1">mdi-information</v-icon>
        <span class="text-caption">{{ score.status }}</span>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { gamesApi } from '@/services/api'
import { formatDate } from '@/utils/dateUtils'
import type { GameListItem, GameScore } from '@/types'

interface Props {
  game: GameListItem
}

const props = defineProps<Props>()

const score = ref<GameScore>({
  game_id: props.game.id,
  team_1: 0,
  team_2: 0,
  status: ''
})

const winner = computed(() => score.value.winner)

const formattedDate = computed(() => {
  const date = new Date(props.game.date)
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
})

onMounted(async () => {
  try {
    const response = await gamesApi.getScore(props.game.id)
    score.value = response.data
  } catch (e) {
    console.error('Failed to fetch score:', e)
  }
})
</script>

<style scoped>
.match-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 4px solid transparent;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 178, 227, 0.3) !important;
  border-left-color: #00B2E3;
}

.score-section {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 20px;
}

.team-score {
  flex: 1;
  text-align: center;
}

.vs-divider {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>