<template>
    <v-card elevation="3">
        <v-card-title class="pa-4">
            <v-icon class="mr-2" color="secondary">mdi-chart-box</v-icon>
            Statistiche
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-4">
            <v-row>
                <v-col cols="6" sm="3">
                    <div class="stat-box">
                        <v-icon size="32" color="secondary" class="mb-2">mdi-soccer</v-icon>
                        <div class="text-h5 font-weight-bold gold-text">{{ stats.total_goals }}</div>
                        <div class="text-caption text-secondary">Goal</div>
                    </div>
                </v-col>

                <v-col cols="6" sm="3">
                    <div class="stat-box">
                        <v-icon size="32" color="accent" class="mb-2">mdi-shoe-cleat</v-icon>
                        <div class="text-h5 font-weight-bold gold-text">{{ stats.total_assists }}</div>
                        <div class="text-caption text-secondary">Assist</div>
                    </div>
                </v-col>

                <v-col cols="6" sm="3">
                    <div class="stat-box">
                        <v-icon size="32" color="success" class="mb-2">mdi-trophy</v-icon>
                        <div class="text-h5 font-weight-bold gold-text">{{ stats.wins }}</div>
                        <div class="text-caption text-secondary">Vittorie</div>
                    </div>
                </v-col>

                <v-col cols="6" sm="3">
                    <div class="stat-box">
                        <v-icon size="32" color="info" class="mb-2">mdi-soccer-field</v-icon>
                        <div class="text-h5 font-weight-bold gold-text">{{ stats.games_played }}</div>
                        <div class="text-caption text-secondary">Partite</div>
                    </div>
                </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <div class="additional-stats">
                <div class="stat-row">
                    <span class="text-body-2 text-secondary">Goal a Partita</span>
                    <span class="text-h6 font-weight-bold">{{ stats.goals_per_game }}</span>
                </div>

                <div class="stat-row">
                    <span class="text-body-2 text-secondary">Win Rate</span>
                    <span class="text-h6 font-weight-bold">{{ winRate }}%</span>
                </div>

                <div class="stat-row">
                    <span class="text-body-2 text-secondary">Contribuzioni Totali</span>
                    <span class="text-h6 font-weight-bold">{{ stats.total_goals + stats.total_assists }}</span>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PlayerStats } from '@/types'

interface Props {
    stats: PlayerStats
}

const props = defineProps<Props>()

const winRate = computed(() => {
    if (props.stats.games_played === 0) return 0
    return Math.round((props.stats.wins / props.stats.games_played) * 100)
})
</script>

<style scoped>
.stat-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background-color: rgba(26, 41, 66, 0.5);
    border-radius: 8px;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-box:hover {
    background-color: rgba(26, 41, 66, 0.7);
    transform: translateY(-2px);
}

.additional-stats {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background-color: rgba(26, 41, 66, 0.3);
    border-radius: 8px;
}
</style>