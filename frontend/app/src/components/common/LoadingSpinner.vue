<template>
    <div class="loading-container">
        <v-progress-circular :size="size" :width="width" color="secondary" indeterminate></v-progress-circular>
        <p v-if="message" class="mt-4 text-secondary">{{ message }}</p>
    </div>
</template>

<script setup lang="ts">
interface Props {
    size?: number
    width?: number
    message?: string
}

withDefaults(defineProps<Props>(), {
    size: 64,
    width: 6,
    message: ''
})
</script>

<style scoped>
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    min-height: 200px;
}
</style>