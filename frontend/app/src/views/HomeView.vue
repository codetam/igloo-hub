<template>
    <v-container class="py-6">
        <!-- Hero Section -->
        <v-card class="mb-6 cl-gradient" elevation="4">
            <v-card-text class="pa-6 text-center">
                <v-icon size="64" class="gold-text mb-2">mdi-trophy</v-icon>
                <h1 class="text-h4 font-weight-bold mb-2">Igloo Hub</h1>
                <p class="text-body-1">Visualizza partite, goal e statistiche.</p>
            </v-card-text>
        </v-card>

        <!-- Quick Actions -->
        <div class="mb-6">
            <h2 class="text-h6 mb-3 ml-2">Quick Actions</h2>
            <v-row>
                <v-col cols="6">
                    <v-card :to="{ name: 'create-match' }" class="text-center pa-4 hover-card" elevation="2">
                        <v-icon size="48" color="secondary" class="mb-2">mdi-plus-circle</v-icon>
                        <div class="text-subtitle-2">Nuova Partita</div>
                    </v-card>
                </v-col>
                <v-col cols="6">
                    <v-card :to="{ name: 'create-player' }" class="text-center pa-4 hover-card" elevation="2">
                        <v-icon size="48" color="accent" class="mb-2">mdi-account-plus</v-icon>
                        <div class="text-subtitle-2">Nuovo Giocatore</div>
                    </v-card>
                </v-col>
            </v-row>
        </div>

        <!-- Recent Matches -->
        <div class="mb-6">
            <div class="d-flex align-center justify-space-between mb-3">
                <h2 class="text-h6 ml-2">Partite Recenti</h2>
                <v-btn :to="{ name: 'matches' }" variant="text" size="small" color="secondary">
                    Altro
                </v-btn>
            </div>

            <LoadingSpinner v-if="gamesStore.loading" message="Caricamento..." />

            <EmptyState v-else-if="recentGames.length === 0" icon="mdi-soccer-field" title="Non ci sono ancora match"
                message="Crea il tuo primo match!" action-text="Crea Partita"
                @action="router.push({ name: 'create-match' })" />

            <div v-else>
                <MatchCard v-for="game in recentGames" :key="game.id" :game="game" class="mb-3" />
            </div>
        </div>

        <!-- Top Players Preview -->
        <div>
            <div class="d-flex align-center justify-space-between mb-3">
                <h2 class="text-h6 ml-2">Giocatori</h2>
                <v-btn :to="{ name: 'players' }" variant="text" size="small" color="secondary">
                    Altro
                </v-btn>
            </div>

            <LoadingSpinner v-if="playersStore.loading" message="Caricamento..." />

            <EmptyState v-else-if="playersStore.players.length === 0" icon="mdi-account-group" title="Non ci sono giocatori"
                message="Aggiungi il tuo primo giocatore!" action-text="Aggiungi Giocatore"
                @action="router.push({ name: 'create-player' })" />

            <v-row v-else>
                <v-col v-for="player in topPlayers" :key="player.id" cols="6" sm="4" md="3">
                    <PlayerCard :player="player" />
                </v-col>
            </v-row>
        </div>
    </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import { usePlayersStore } from '@/stores/players'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import MatchCard from '@/components/match/MatchCard.vue'
import PlayerCard from '@/components/player/PlayerCard.vue'

const router = useRouter()
const gamesStore = useGamesStore()
const playersStore = usePlayersStore()

const recentGames = computed(() => gamesStore.games.slice(0, 5))
const topPlayers = computed(() => playersStore.players.slice(0, 8))

onMounted(async () => {
    await Promise.all([
        gamesStore.fetchGames(),
        playersStore.fetchPlayers()
    ])
})
</script>

<style scoped>
.hover-card {
    transition: all 0.3s ease;
    cursor: pointer;
}

.hover-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 178, 227, 0.3) !important;
}
</style>