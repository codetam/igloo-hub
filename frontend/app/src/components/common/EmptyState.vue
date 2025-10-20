<template>
    <div class="empty-state">
        <v-icon :size="iconSize" color="surface-variant" class="mb-4">
            {{ icon }}
        </v-icon>
        <h3 class="text-h6 mb-2">{{ title }}</h3>
        <p class="text-body-2 text-medium-emphasis mb-4">{{ message }}</p>
        <v-btn v-if="actionText" color="secondary" :prepend-icon="actionIcon" @click="$emit('action')">
            {{ actionText }}
        </v-btn>
    </div>
</template>

<script setup lang="ts">
interface Props {
    icon?: string
    iconSize?: number
    title: string
    message: string
    actionText?: string
    actionIcon?: string
}

withDefaults(defineProps<Props>(), {
    icon: 'mdi-information-outline',
    iconSize: 80,
    actionIcon: 'mdi-plus'
})

defineEmits<{
    action: []
}>()
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    text-align: center;
    min-height: 300px;
}
</style>