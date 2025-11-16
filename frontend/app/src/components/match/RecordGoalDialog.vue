<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600">
    <v-card>
      <v-card-title class="pa-4 cl-gradient">
        <v-icon class="mr-2" size="28">mdi-soccer</v-icon>
        Aggiungi Goal
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="valid">
          <!-- Team Selection -->
          <v-radio-group v-model="formData.team_id" inline :rules="[(v) => v !== null || 'Team is required']">
            <template v-slot:label>
              <div class="text-subtitle-2 mb-2">Team che ha segnato *</div>
            </template>
            <v-radio :value="game.home_team.id" color="secondary">
              <template v-slot:label>
                <div class="d-flex align-center">
                  <v-icon color="secondary" class="mr-1">mdi-shield</v-icon>
                  Team Casa
                </div>
              </template>
            </v-radio>
            <v-radio :value="game.away_team.id" color="accent">
              <template v-slot:label>
                <div class="d-flex align-center">
                  <v-icon color="accent" class="mr-1">mdi-shield</v-icon>
                  Team Fuori Casa
                </div>
              </template>
            </v-radio>
          </v-radio-group>

          <!-- Scorer Selection -->
          <v-select v-model="formData.scorer_id" :items="availablePlayers" item-title="name" item-value="id"
            label="Marcatore *" :rules="[(v) => !!v || 'Scorer is required']" prepend-inner-icon="mdi-account"
            :disabled="!formData.team_id" required>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <template v-slot:prepend>
                  <v-avatar :color="formData.team_id === game.home_team.id ? 'secondary' : 'accent'" size="32">
                    <v-icon size="20">mdi-account</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                <v-list-item-subtitle v-if="item.raw.nickname">
                  "{{ item.raw.nickname }}"
                </v-list-item-subtitle>
              </v-list-item>
            </template>
          </v-select>

          <!-- Assister Selection (Optional) -->
          <v-select v-model="formData.assister_id" :items="availableAssisters" item-title="name" item-value="id"
            label="Assist-Man (Opzionale)" prepend-inner-icon="mdi-hand-pointing-right" :disabled="!formData.scorer_id"
            clearable>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <template v-slot:prepend>
                  <v-avatar :color="formData.team_id === game.home_team.id ? 'secondary' : 'accent'" size="32">
                    <v-icon size="20">mdi-account</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                <v-list-item-subtitle v-if="item.raw.nickname">
                  "{{ item.raw.nickname }}"
                </v-list-item-subtitle>
              </v-list-item>
            </template>
          </v-select>

          <v-alert type="info" variant="tonal" class="mt-4">
            <v-icon start>mdi-clock-outline</v-icon>
            Il minuto del goal è registrato automaticamente
          </v-alert>

          <v-alert v-if="error" type="error" class="mt-4" closable @click:close="error = null">
            {{ error }}
          </v-alert>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-btn variant="text" @click="closeDialog" :disabled="submitting">
          Annulla
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="accent" :loading="submitting" :disabled="!valid" @click="submitGoal">
          Registra Goal
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { useGamesStore } from '@/stores/games'
import type { Game } from '@/types'

interface Props {
  modelValue: boolean
  game: Game
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'goal-recorded': []
}>()

const gamesStore = useGamesStore()
const formRef = ref()
const valid = ref(false)
const submitting = ref(false)
const error = ref<string | null>(null)

const formData = reactive<{
  team_id: string | null
  scorer_id: string
  assister_id: string
}>({
  team_id: null,
  scorer_id: '',
  assister_id: ''
})

const availablePlayers = computed(() => {
  if (!formData.team_id) return []
  return formData.team_id === props.game.home_team.id ? props.game.home_team.players : props.game.away_team.players
})

const availableAssisters = computed(() => {
  return availablePlayers.value.filter(p => p.id !== formData.scorer_id)
})

watch(() => formData.team_id, () => {
  formData.scorer_id = ''
  formData.assister_id = ''
})

watch(() => formData.scorer_id, () => {
  if (formData.assister_id === formData.scorer_id) {
    formData.assister_id = ''
  }
})

async function submitGoal() {
  if (!valid.value || !formData.team_id) return

  submitting.value = true
  error.value = null

  try {
    // Get current UTC time as ISO string
    const currentUtcTime = new Date().toISOString()

    await gamesStore.recordGoal(props.game.id, {
      team_id: formData.team_id,
      scorer_id: formData.scorer_id,
      assister_id: formData.assister_id || undefined,
      minute: currentUtcTime
    })

    emit('goal-recorded')
    closeDialog()
  } catch (e) {
    error.value = 'Failed to record goal. Please try again.'
    console.error(e)
  } finally {
    submitting.value = false
  }
}

function closeDialog() {
  emit('update:modelValue', false)
  resetForm()
}

function resetForm() {
  formData.team_id = null
  formData.scorer_id = ''
  formData.assister_id = ''
  error.value = null
}
</script>

<style scoped>
/* Additional styles if needed */
</style>