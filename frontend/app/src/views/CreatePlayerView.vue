<template>
    <v-container class="py-6">
        <v-card max-width="600" class="mx-auto" elevation="4">
            <v-card-title class="text-h5 pa-6 cl-gradient">
                <v-icon class="mr-2" size="32">mdi-account-plus</v-icon>
                Aggiungi Giocatore
            </v-card-title>

            <v-card-text class="pa-6">
                <v-form ref="formRef" v-model="valid" @submit.prevent="handleSubmit">
                    <v-text-field v-model="formData.name" label="Nome *" :rules="nameRules"
                        prepend-inner-icon="mdi-account" required autofocus></v-text-field>

                    <v-text-field v-model="formData.nickname" label="Nickname (Opzionale)"
                        prepend-inner-icon="mdi-account-star" hint="" persistent-hint></v-text-field>

                    <v-alert v-if="error" type="error" class="mt-4" closable @click:close="error = null">
                        {{ error }}
                    </v-alert>

                    <v-alert v-if="success" type="success" class="mt-4">
                        Giocatore creato con successo!
                    </v-alert>
                </v-form>
            </v-card-text>

            <v-card-actions class="pa-6 pt-0">
                <v-btn variant="text" @click="router.back()" :disabled="submitting">
                    Annulla
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn color="accent" :loading="submitting" :disabled="!valid" @click="handleSubmit">
                    Crea Giocatore
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { usePlayersStore } from '@/stores/players'

const router = useRouter()
const playersStore = usePlayersStore()

const formRef = ref()
const valid = ref(false)
const submitting = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

const formData = reactive({
    name: '',
    nickname: ''
})

const nameRules = [
    (v: string) => !!v || 'Il nome non può essere vuoto',
    (v: string) => v.length >= 2 || 'Il nome deve avere almeno 2 caratteri',
    (v: string) => v.length <= 100 || 'Il nome deve avere meno di 100 caratteri',
]

async function handleSubmit() {
    if (!valid.value) return

    submitting.value = true
    error.value = null
    success.value = false

    try {
        await playersStore.createPlayer({
            name: formData.name,
            nickname: formData.nickname || undefined
        })

        success.value = true

        // Redirect after short delay
        setTimeout(() => {
            router.push({ name: 'players' as any })
        }, 1000)
    } catch (e) {
        error.value = 'Creazione giocatore fallita. Riprova.'
        console.error(e)
    } finally {
        submitting.value = false
    }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>