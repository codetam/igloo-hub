<template>
  <v-card elevation="3">
    <v-card-title class="pa-4">
      <v-icon class="mr-2" color="accent">mdi-soccer</v-icon>
      Timeline Goal
      <v-chip size="small" class="ml-2">{{ goals.length }}</v-chip>
    </v-card-title>

    <v-divider></v-divider>

    <v-card-text class="pa-4">
      <v-timeline side="end" truncate-line="both" density="compact">
        <v-timeline-item
          v-for="goal in sortedGoals"
          :key="goal.id"
          :dot-color="goal.team === 1 ? 'secondary' : 'accent'"
          size="small"
        >
          <template v-slot:opposite>
            <div class="text-caption">
              {{ formatGoalMinute(goal.minute) }}
            </div>
          </template>

          <v-card elevation="2" class="goal-card">
            <v-card-text class="pa-3">
              <div class="d-flex align-center mb-1">
                <v-chip
                  :color="goal.team === 1 ? 'secondary' : 'accent'"
                  size="x-small"
                  class="mr-2"
                >
                  Team {{ goal.team }}
                </v-chip>
                <v-icon size="16" class="mr-1">mdi-soccer</v-icon>
                <span class="text-body-2 font-weight-bold">
                  {{ goal.scorer.name }}
                </span>
              </div>

              <div v-if="goal.assister" class="d-flex align-center text-caption text-secondary">
                <v-icon size="14" class="mr-1">mdi-hand-pointing-right</v-icon>
                Assist: {{ goal.assister.name }}
              </div>
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Goal } from '@/types'

interface Props {
  goals: Goal[]
  gameStartTime: string // Game start datetime
}

const props = defineProps<Props>()

const sortedGoals = computed(() => {
  return [...props.goals].sort((a, b) => {
    if (!a.minute && !b.minute) return 0
    if (!a.minute) return 1
    if (!b.minute) return -1
    return new Date(a.minute).getTime() - new Date(b.minute).getTime()
  })
})

function formatGoalMinute(goalTime?: string): string {
  if (!goalTime) return '-'
  
  const gameStart = new Date(props.gameStartTime)
  const goalMoment = new Date(goalTime)
  
  // Calculate difference in minutes
  const diffMs = goalMoment.getTime() - gameStart.getTime()
  const diffMinutes = Math.floor(diffMs / 60000)
  
  if (diffMinutes < 0) return '0\''
  
  return `${diffMinutes}'`
}
</script>

<style scoped>
.goal-card {
  transition: all 0.2s ease;
}

.goal-card:hover {
  transform: translateX(4px);
}
</style>