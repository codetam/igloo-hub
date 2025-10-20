<template>
    <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600">
        <v-card>
            <v-card-title class="d-flex align-center pa-4">
                <v-icon class="mr-2">mdi-account-search</v-icon>
                Seleziona Giocatore
                <v-spacer></v-spacer>
                <v-btn icon="mdi-close" variant="text" @click="$emit('update:modelValue', false)"></v-btn>
            </v-card-title>

            <v-card-text>
                <v-text-field v-model="searchQuery" prepend-inner-icon="mdi-magnify" label="Ricerca giocatori..." clearable
                    autofocus class="mb-4"></v-text-field>

                <LoadingSpinner v-if="loading" message="Caricamento..." />

                <EmptyState v-else-if="filteredPlayers.length === 0" icon="mdi-account-off" title="Nessun giocatore trovato"
                    message="Prova a cambiare i termini di ricerca" :icon-size="64" />

                <v-list v-else class="player-list">
                    <v-list-item v-for="player in filteredPlayers" :key="player.id" @click="selectPlayer(player)"
                        :disabled="excludeIds.includes(player.id)">
                        <template v-slot:prepend>
                            <v-avatar color="secondary">
                                <v-icon>mdi-account</v-icon>
                            </v-avatar>
                        </template>

                        <v-list-item-title>{{ player.name }}</v-list-item-title>
                        <v-list-item-subtitle v-if="player.nickname">
                            "{{ player.nickname }}"
                        </v-list-item-subtitle>

                        <template v-slot:append>
                            <v-chip v-if="excludeIds.includes(player.id)" size="small" color="surface-variant">
                                Già aggiunto
                            </v-chip>
                        </template>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { usePlayersStore } from '@/stores/players'
import type { Player } from '@/types'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

interface Props {
    modelValue: boolean
    excludeIds?: string[]
}

const props = withDefaults(defineProps<Props>(), {
    excludeIds: () => []
})

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    'select': [player: Player]
}>()

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

function selectPlayer(player: Player) {
    if (props.excludeIds.includes(player.id)) return
    emit('select', player)
    emit('update:modelValue', false)
    searchQuery.value = ''
}

watch(() => props.modelValue, async (newVal) => {
    if (newVal && playersStore.players.length === 0) {
        loading.value = true
        await playersStore.fetchPlayers()
        loading.value = false
    }
})

onMounted(async () => {
    if (playersStore.players.length === 0) {
        loading.value = true
        await playersStore.fetchPlayers()
        loading.value = false
    }
})
</script>

<style scoped>
.player-list {
    max-height: 400px;
    overflow-y: auto;
}
</style>