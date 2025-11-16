<template>
    <v-container class="py-6">
        <!-- Header -->
        <div class="d-flex align-center justify-space-between mb-6">
            <h1 class="text-h4 font-weight-bold">Giocatori</h1>
            <v-btn color="accent" :to="{ name: 'create-player' }" prepend-icon="mdi-account-plus">
                Aggiungi Giocatore
            </v-btn>
        </div>

        <!-- Search Bar -->
        <v-text-field v-model="searchQuery" prepend-inner-icon="mdi-magnify" label="Ricerca giocatore..." clearable
            class="mb-4" @input="handleSearch"></v-text-field>

        <!-- Players Grid -->
        <LoadingSpinner v-if="loading" message="Caricamento..." />

        <EmptyState v-else-if="filteredPlayers.length === 0 && !searchQuery" icon="mdi-account-group"
            title="Non ci sono giocatori" message="Aggiungi il tuo primo giocatore!" action-text="Aggiungi Giocatore"
            @action="router.push({ name: 'create-player' as any })" />

        <EmptyState v-else-if="filteredPlayers.length === 0 && searchQuery" icon="mdi-account-search"
            title="Non ci sono giocatori" message="Prova un altro termine di ricerca" />

        <v-row v-else>
            <v-col v-for="player in filteredPlayers" :key="player.id" cols="6" sm="4" md="3" lg="2">
                <PlayerCard :player="player" />
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlayersStore } from '@/stores/players'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import PlayerCard from '@/components/player/PlayerCard.vue'

const router = useRouter()
const playersStore = usePlayersStore()
const searchQuery = ref('')
const loading = ref(false)

const filteredPlayers = computed(() => {
    if (!searchQuery.value) {
        return playersStore.players
    }
    const query = searchQuery.value.toLowerCase()
    return playersStore.players.filter(player =>
        player.name.toLowerCase().includes(query) ||
        player.nickname?.toLowerCase().includes(query)
    )
})

async function handleSearch() {
    // Real-time filtering is done via computed property
    // Could also implement server-side search here if needed
}

onMounted(async () => {
    loading.value = true
    await playersStore.fetchPlayers()
    loading.value = false
})
</script>

<style scoped>
/* Additional styles if needed */
</style>