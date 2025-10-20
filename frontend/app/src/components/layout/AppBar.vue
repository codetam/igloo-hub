<template>
    <v-app-bar :elevation="2" class="app-bar" color="primary">
        <v-app-bar-nav-icon v-if="showBackButton" @click="goBack" class="hide-on-desktop">
            <v-icon>mdi-arrow-left</v-icon>
        </v-app-bar-nav-icon>

        <v-toolbar-title class="d-flex align-center">
            <v-icon size="32" class="mr-2 gold-text">mdi-soccer</v-icon>
            <span class="font-weight-bold">Igloo Hub</span>
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <!-- Desktop Navigation -->
        <div class="hide-on-mobile">
            <v-btn :to="{ name: 'home' }" :class="{ 'active-route': isActiveRoute('home') }" variant="text">
                <v-icon start>mdi-home</v-icon>
                Home
            </v-btn>
            <v-btn :to="{ name: 'matches' }" :class="{ 'active-route': isActiveRoute('matches') }" variant="text">
                <v-icon start>mdi-soccer-field</v-icon>
                Partite
            </v-btn>
            <v-btn :to="{ name: 'players' }" :class="{ 'active-route': isActiveRoute('players') }" variant="text">
                <v-icon start>mdi-account-group</v-icon>
                Giocatori
            </v-btn>
        </div>

        <!-- Quick Action Button -->
        <v-menu location="bottom">
            <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props" color="accent" class="ml-2">
                    <v-icon>mdi-plus-circle</v-icon>
                </v-btn>
            </template>
            <v-list>
                <v-list-item :to="{ name: 'create-match' }" prepend-icon="mdi-soccer-field">
                    <v-list-item-title>Nuova Partita</v-list-item-title>
                </v-list-item>
                <v-list-item :to="{ name: 'create-player' }" prepend-icon="mdi-account-plus">
                    <v-list-item-title>Nuovo Giocatore</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const showBackButton = computed(() => {
    const routesWithBack = [
        'player-detail',
        'match-detail',
        'create-player',
        'create-match'
    ]
    return routesWithBack.includes(route.name as string)
})

function isActiveRoute(routeName: string): boolean {
    return route.name === routeName
}

function goBack() {
    router.back()
}
</script>

<style scoped>
.app-bar {
    background: linear-gradient(90deg, #001E40 0%, #003366 100%) !important;
}

.active-route {
    background-color: rgba(0, 178, 227, 0.2);
    color: #00B2E3;
}

.v-btn {
    text-transform: none;
}
</style>