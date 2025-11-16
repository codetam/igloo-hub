<template>
    <v-card elevation="3" :class="teamClass">
        <v-card-title class="d-flex align-center pa-4">
            <v-icon :color="teamColor" class="mr-2" size="28">mdi-shield</v-icon>
            <span class="text-h6">Team {{ (team.id === game.home_team.id) ? "Casa" : "Fuori Casa" }}</span>
            <v-chip size="small" class="ml-2">{{ team.players.length }}</v-chip>
            <v-spacer></v-spacer>
            <v-btn icon="mdi-account-plus" size="small" :color="teamColor" variant="text"
                @click="$emit('add-player')"></v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-0">
            <v-list v-if="team.players.length > 0">
                <v-list-item v-for="player in team.players" :key="player.id"
                    :to="{ name: 'player-detail', params: { id: player.id } }">
                    <template v-slot:prepend>
                        <v-avatar :color="teamColor" size="40">
                            <v-icon>mdi-account</v-icon>
                        </v-avatar>
                    </template>

                    <v-list-item-title>{{ player.name }}</v-list-item-title>
                    <v-list-item-subtitle v-if="player.nickname">
                        "{{ player.nickname }}"
                    </v-list-item-subtitle>

                    <template v-slot:append>
                        <div class="d-flex gap-2">
                            <v-chip v-if="player.goals && player.goals > 0" size="small" color="secondary">
                                <v-icon start size="14">mdi-soccer</v-icon>
                                {{ player.goals }}
                            </v-chip>
                            <v-chip v-if="player.assists && player.assists > 0" size="small" color="accent">
                                <v-icon start size="14">mdi-shoe-cleat</v-icon>
                                {{ player.assists }}
                            </v-chip>
                        </div>
                    </template>
                </v-list-item>
            </v-list>

            <EmptyState v-else icon="mdi-account-group-outline" title="Non ci sono giocatori"
                message="Aggiungi giocatori al team" :icon-size="48" action-text="Aggiungi Giocatore"
                @action="$emit('add-player')" />
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import EmptyState from '@/components/common/EmptyState.vue'
import type { Game, GameTeamRead } from '@/types';

interface Props {
    game: Game,
    team: GameTeamRead
}

const props = defineProps<Props>()

defineEmits<{
    'add-player': []
}>()

const teamColor = computed(() => props.team.id === props.game.home_team.id ? 'secondary' : 'accent')
const teamClass = computed(() => `team-${props.team.id === props.game.home_team.id ? 1 : 2}-card`)
</script>

<style scoped>
.team-1-card {
    border-left: 4px solid #00B2E3;
}

.team-2-card {
    border-left: 4px solid #FFD700;
}
</style>