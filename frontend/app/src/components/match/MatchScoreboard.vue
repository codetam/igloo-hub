<template>
    <div class="scoreboard">
        <div class="team-score-large">
            <div class="team-label">
                <v-icon color="secondary" size="32">mdi-shield</v-icon>
                <span class="text-h6">Team 1</span>
            </div>
            <div class="score-display">{{ score.home_team }}</div>
        </div>

        <div class="score-divider">
            <v-icon size="40" color="accent">mdi-minus</v-icon>
        </div>

        <div class="team-score-large">
            <div class="team-label">
                <v-icon color="accent" size="32">mdi-shield</v-icon>
                <span class="text-h6">Team 2</span>
            </div>
            <div class="score-display">{{ score.away_team }}</div>
        </div>
    </div>

    <div v-if="winner" class="text-center mt-4">
        <v-chip :color="winner === 1 ? 'secondary' : 'accent'" size="large" prepend-icon="mdi-trophy" class="px-6">
            Team {{ winner }} Vince!
        </v-chip>
    </div>

    <div v-else-if="score.home_team > 0" class="text-center mt-4">
        <v-chip color="warning" size="large" prepend-icon="mdi-equal" class="px-6">
            Pareggio
        </v-chip>
    </div>
</template>

<script setup lang="ts">
import type { GameScore } from '@/types'

interface Props {
    score: GameScore
}

const props = defineProps<Props>()

const winner = computed(() => {
    if (props.score.home_team > props.score.away_team) {
        return 1;
    }
    else if (props.score.away_team > props.score.home_team) {
        return 2;
    }
    else return null;
})

</script>

<style scoped>
.scoreboard {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    padding: 20px;
    background: linear-gradient(135deg, rgba(0, 30, 64, 0.5) 0%, rgba(0, 178, 227, 0.1) 100%);
    border-radius: 12px;
}

.team-score-large {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}

.team-label {
    display: flex;
    align-items: center;
    gap: 8px;
}

.score-display {
    font-size: 64px;
    font-weight: bold;
    line-height: 1;
    color: #FFD700;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.score-divider {
    display: flex;
    align-items: center;
}

@media (max-width: 600px) {
    .scoreboard {
        gap: 20px;
        padding: 16px;
    }

    .score-display {
        font-size: 48px;
    }

    .team-label span {
        font-size: 1rem;
    }
}
</style>