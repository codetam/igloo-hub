<template>
  <v-card :to="{ name: 'match-detail', params: { id: game.id } }" class="match-card" elevation="2" hover>
    <v-card-text class="pa-4">
      <!-- Date and Stadium -->
      <div class="d-flex align-center mb-3">
        <v-icon size="20" class="mr-2 text-secondary">mdi-calendar</v-icon>
        <span class="text-caption">{{ formattedDate }}</span>
        <v-spacer></v-spacer>
        <v-chip size="small" color="surface-variant">
          <v-icon start size="16">mdi-map-marker</v-icon>
          {{ game.stadium?.name }}
        </v-chip>
      </div>

      <!-- Score Display -->
      <div class="score-section">
        <div class="team-score">
          <div class="text-h5 font-weight-bold">{{ score.home_team }}</div>
          <div class="text-caption text-secondary">Team Casa</div>
        </div>

        <div class="vs-divider">
          <v-icon size="24" color="accent">mdi-sword-cross</v-icon>
        </div>

        <div class="team-score">
          <div class="text-h5 font-weight-bold">{{ score.away_team }}</div>
          <div class="text-caption text-secondary">Team Fuori Casa</div>
        </div>
      </div>

      <!-- Winner Badge -->
      <div v-if="winner" class="text-center mt-3">
        <v-chip :color="winner === 1 ? 'secondary' : 'accent'" size="small" prepend-icon="mdi-trophy">
          Team {{ winner }} Vince
        </v-chip>
      </div>

      <!-- Draw -->
      <div v-else-if="score.home_team === score.away_team && (score.home_team > 0 || score.away_team > 0)"
        class="text-center mt-3">
        <v-chip size="small" color="warning">
          Pareggio
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { gamesApi } from '@/services/api'
import type { Game, GameScore } from '@/types'

interface Props {
  game: Game
}

const props = defineProps<Props>()

const score = ref<GameScore>({
  home_team: 0,
  away_team: 0,
})

const winner = computed(() => {
  if (score.value.home_team > score.value.away_team) {
    return 1;
  }
  else if (score.value.away_team > score.value.home_team) {
    return 2;
  }
  else return null;
})

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
    const response = await gamesApi.getById(props.game.id)
    score.value = response.data.score
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