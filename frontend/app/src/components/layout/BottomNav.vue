<template>
    <v-bottom-navigation v-model="activeTab" class="hide-on-desktop bottom-nav" color="secondary" bg-color="primary"
        grow>
        <v-btn :value="'home'" @click="navigateTo('home')">
            <v-icon>mdi-home</v-icon>
            <span>Home</span>
        </v-btn>

        <v-btn :value="'matches'" @click="navigateTo('matches')">
            <v-icon>mdi-soccer-field</v-icon>
            <span>Partite</span>
        </v-btn>

        <v-btn :value="'players'" @click="navigateTo('players')">
            <v-icon>mdi-account-group</v-icon>
            <span>Giocatori</span>
        </v-btn>
    </v-bottom-navigation>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const activeTab = ref('home')

// Update active tab based on current route
watch(() => route.name, (newRoute) => {
    const routeName = newRoute as string
    if (routeName === 'home') {
        activeTab.value = 'home'
    } else if (['matches', 'match-detail', 'create-match'].includes(routeName)) {
        activeTab.value = 'matches'
    } else if (['players', 'player-detail', 'create-player'].includes(routeName)) {
        activeTab.value = 'players'
    }
}, { immediate: true })

function navigateTo(name: string) {
    router.push({ name: name as any })
}
</script>

<style scoped>
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    border-top: 1px solid rgba(0, 178, 227, 0.3);
}

.v-btn {
    height: 100%;
    flex-direction: column;
    font-size: 12px;
}

.v-btn span {
    margin-top: 4px;
}
</style>