<template>
    <v-card :to="{ name: 'player-detail', params: { id: player.id } }" class="player-card" elevation="2" hover>
        <v-card-text class="pa-4 text-center">
            <v-avatar size="64" color="secondary" class="mb-3">
                <v-icon size="40" color="white">mdi-account</v-icon>
            </v-avatar>

            <div class="text-subtitle-1 font-weight-bold text-truncate">
                {{ player.name }}
            </div>

            <div v-if="player.nickname" class="text-caption text-secondary text-truncate">
                "{{ player.nickname }}"
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
import type { Player } from '@/types'

interface Props {
    player: Player
}

defineProps<Props>()
</script>

<style scoped>
.player-card {
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
}

.player-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 178, 227, 0.3) !important;
}
</style>