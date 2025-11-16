<template>
    <v-container class="py-6">
        <!-- Header -->
        <div class="d-flex align-center justify-space-between mb-6">
            <h1 class="text-h4 font-weight-bold">Partite</h1>
            <v-btn color="accent" :to="{ name: 'create-match' }" prepend-icon="mdi-plus-circle">
                Nuova Partita
            </v-btn>
        </div>

        <!-- Loading State -->
        <LoadingSpinner v-if="loading" message="Caricamento..." />

        <!-- Empty State -->
        <EmptyState v-else-if="gamesStore.games.length === 0" icon="mdi-soccer-field" title="Non ci sono ancora partite"
            message="Crea la tua prima partita!" action-text="Crea Partita"
            @action="router.push({ name: 'create-match' as any })" />

        <!-- Matches List -->
        <div v-else class="matches-list">
            <MatchCard v-for="game in gamesStore.games" :key="game.id" :game="game" class="mb-3" />
        </div>
    </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import MatchCard from '@/components/match/MatchCard.vue'

const router = useRouter()
const gamesStore = useGamesStore()
const loading = ref(false)

onMounted(async () => {
    loading.value = true
    await gamesStore.fetchGames()
    loading.value = false
})
</script>

<style scoped>
.matches-list {
    max-width: 800px;
    margin: 0 auto;
}
</style>