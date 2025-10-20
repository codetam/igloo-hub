<template>
  <v-container class="py-6">
    <v-card max-width="900" class="mx-auto" elevation="4">
      <v-card-title class="text-h5 pa-6 cl-gradient">
        <v-icon class="mr-2" size="32">mdi-soccer-field</v-icon>
        Crea nuova Partita
      </v-card-title>

      <v-card-text class="pa-6">
        <v-stepper v-model="step" :items="['Dettagli', 'Aggiungi Giocatori']">
          <!-- Step 1: Match Details -->
          <v-stepper-window>
            <v-stepper-window-item :value="1">
              <v-form ref="formRef" v-model="valid">
                <v-select
                  v-model="formData.stadium_id"
                  :items="stadiumOptions"
                  item-title="name"
                  item-value="id"
                  label="Stadio *"
                  :rules="[(v) => !!v || 'Lo stadio non può essere vuoto!']"
                  prepend-inner-icon="mdi-map-marker"
                  required
                >
                  <template v-slot:append>
                    <v-btn
                      icon="mdi-plus"
                      size="small"
                      variant="text"
                      @click="showCreateStadium = true"
                    ></v-btn>
                  </template>
                </v-select>

                <v-text-field
                  v-model="formData.date"
                  label="Data *"
                  type="datetime-local"
                  :rules="[(v) => !!v || 'La data non può essere vuota!']"
                  prepend-inner-icon="mdi-calendar"
                  required
                ></v-text-field>

                <v-textarea
                  v-model="formData.notes"
                  label="Note (Opzionale)"
                  prepend-inner-icon="mdi-note-text"
                  rows="3"
                  hint=""
                  persistent-hint
                ></v-textarea>
              </v-form>
            </v-stepper-window-item>

            <!-- Step 2: Add Players -->
            <v-stepper-window-item :value="2">
              <v-alert type="info" class="mb-4">
                Aggiungi giocatori in ciascuna squadra. Puoi aggiungere altri giocatori successivamente.
              </v-alert>

              <v-row>
                <!-- Team 1 -->
                <v-col cols="12" md="6">
                  <div class="team-section">
                    <h3 class="text-h6 mb-3 d-flex align-center">
                      <v-icon color="secondary" class="mr-2">mdi-shield</v-icon>
                      Team 1
                      <v-chip size="small" class="ml-2">{{ team1Players.length }}</v-chip>
                    </h3>
                    
                    <v-btn
                      block
                      variant="outlined"
                      color="secondary"
                      prepend-icon="mdi-account-plus"
                      @click="openPlayerDialog(1)"
                      class="mb-3"
                    >
                      Aggiungi Giocatore
                    </v-btn>

                    <v-list v-if="team1Players.length > 0">
                      <v-list-item
                        v-for="player in team1Players"
                        :key="player.id"
                      >
                        <template v-slot:prepend>
                          <v-avatar color="secondary" size="32">
                            <v-icon size="20">mdi-account</v-icon>
                          </v-avatar>
                        </template>
                        <v-list-item-title>{{ player.name }}</v-list-item-title>
                        <v-list-item-subtitle v-if="player.nickname">
                          "{{ player.nickname }}"
                        </v-list-item-subtitle>
                        <template v-slot:append>
                          <v-btn
                            icon="mdi-close"
                            size="small"
                            variant="text"
                            @click="removePlayer(1, player.id)"
                          ></v-btn>
                        </template>
                      </v-list-item>
                    </v-list>
                    <EmptyState
                      v-else
                      icon="mdi-account-group-outline"
                      title="Non ci sono giocatori"
                      message="Aggiungi giocatori al Team 1"
                      :icon-size="48"
                    />
                  </div>
                </v-col>

                <!-- Team 2 -->
                <v-col cols="12" md="6">
                  <div class="team-section">
                    <h3 class="text-h6 mb-3 d-flex align-center">
                      <v-icon color="accent" class="mr-2">mdi-shield</v-icon>
                      Team 2
                      <v-chip size="small" class="ml-2">{{ team2Players.length }}</v-chip>
                    </h3>
                    
                    <v-btn
                      block
                      variant="outlined"
                      color="accent"
                      prepend-icon="mdi-account-plus"
                      @click="openPlayerDialog(2)"
                      class="mb-3"
                    >
                      Aggiungi Giocatore
                    </v-btn>

                    <v-list v-if="team2Players.length > 0">
                      <v-list-item
                        v-for="player in team2Players"
                        :key="player.id"
                      >
                        <template v-slot:prepend>
                          <v-avatar color="accent" size="32">
                            <v-icon size="20">mdi-account</v-icon>
                          </v-avatar>
                        </template>
                        <v-list-item-title>{{ player.name }}</v-list-item-title>
                        <v-list-item-subtitle v-if="player.nickname">
                          "{{ player.nickname }}"
                        </v-list-item-subtitle>
                        <template v-slot:append>
                          <v-btn
                            icon="mdi-close"
                            size="small"
                            variant="text"
                            @click="removePlayer(2, player.id)"
                          ></v-btn>
                        </template>
                      </v-list-item>
                    </v-list>
                    <EmptyState
                      v-else
                      icon="mdi-account-group-outline"
                      title="Non ci sono giocatori"
                      message="Aggiungi giocatori al Team 2"
                      :icon-size="48"
                    />
                  </div>
                </v-col>
              </v-row>
            </v-stepper-window-item>
          </v-stepper-window>

          <template #actions>
            <v-stepper-actions
              @click:next="nextStep"
              @click:prev="step--"
              :disabled="step === 1 ? !valid : false"
              next-text="Avanti"
              prev-text="Indietro"
            />
          </template>
        </v-stepper>

        <v-alert
          v-if="error"
          type="error"
          class="mt-4"
          closable
          @click:close="error = null"
        >
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>

    <!-- Player Selection Dialog -->
    <PlayerSearchDialog
      v-model="showPlayerDialog"
      :exclude-ids="excludedPlayerIds"
      @select="handlePlayerSelect"
    />

    <!-- Create Stadium Dialog -->
    <v-dialog v-model="showCreateStadium" max-width="500">
      <v-card>
        <v-card-title>Create Stadium</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newStadiumName"
            label="Nome Stadio *"
            prepend-inner-icon="mdi-map-marker"
          ></v-text-field>
          <v-text-field
            v-model="newStadiumAddress"
            label="Indirizzo (Opzionale)"
            prepend-inner-icon="mdi-map"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showCreateStadium = false">Annulla</v-btn>
          <v-btn color="primary" @click="createStadium">Crea</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import { useStadiumsStore } from '@/stores/stadiums'
import { getCurrentDateTimeLocalUTCPlus2, dateTimeLocalToUTC } from '@/utils/dateUtils'
import type { Player } from '@/types'
import EmptyState from '@/components/common/EmptyState.vue'
import PlayerSearchDialog from '@/components/player/PlayerSearchDialog.vue'

const router = useRouter()
const gamesStore = useGamesStore()
const stadiumsStore = useStadiumsStore()

const step = ref(1)
const formRef = ref()
const valid = ref(false)
const error = ref<string | null>(null)
const showPlayerDialog = ref(false)
const selectedTeam = ref<1 | 2>(1)
const showCreateStadium = ref(false)
const newStadiumName = ref('')
const newStadiumAddress = ref('')

const formData = reactive({
  stadium_id: '',
  date: getCurrentDateTimeLocalUTCPlus2(),
  notes: ''
})

const team1Players = ref<Player[]>([])
const team2Players = ref<Player[]>([])

const stadiumOptions = computed(() => stadiumsStore.stadiums)

const excludedPlayerIds = computed(() => {
  return [...team1Players.value, ...team2Players.value].map(p => p.id)
})

function openPlayerDialog(team: 1 | 2) {
  selectedTeam.value = team
  showPlayerDialog.value = true
}

function handlePlayerSelect(player: Player) {
  if (selectedTeam.value === 1) {
    team1Players.value.push(player)
  } else {
    team2Players.value.push(player)
  }
}

function removePlayer(team: 1 | 2, playerId: string) {
  if (team === 1) {
    team1Players.value = team1Players.value.filter(p => p.id !== playerId)
  } else {
    team2Players.value = team2Players.value.filter(p => p.id !== playerId)
  }
}

async function nextStep() {
  if (step.value === 1) {
    step.value = 2
  } else {
    await createMatch()
  }
}

async function createMatch() {
  error.value = null

  try {
    // Convert datetime from UTC+2 to UTC for backend
    const utcDate = dateTimeLocalToUTC(formData.date)
    
    // Create the match
    const game = await gamesStore.createGame({
      stadium_id: formData.stadium_id,
      date: utcDate,
      notes: formData.notes || undefined
    })

    // Add players to teams
    const addPlayerPromises = [
      ...team1Players.value.map(p => 
        gamesStore.addPlayerToGame(game.id, { player_id: p.id, team: 1 })
      ),
      ...team2Players.value.map(p => 
        gamesStore.addPlayerToGame(game.id, { player_id: p.id, team: 2 })
      )
    ]

    await Promise.all(addPlayerPromises)

    // Navigate to match detail
    router.push({ name: 'match-detail', params: { id: game.id } })
  } catch (e) {
    error.value = 'Creazione partita fallita. Riprova.'
    console.error(e)
  }
}

async function createStadium() {
  if (!newStadiumName.value) return

  try {
    const stadium = await stadiumsStore.createStadium(
      newStadiumName.value,
      newStadiumAddress.value || undefined
    )
    formData.stadium_id = stadium.id
    showCreateStadium.value = false
    newStadiumName.value = ''
    newStadiumAddress.value = ''
  } catch (e) {
    console.error('Creazione stadio fallita:', e)
  }
}

onMounted(async () => {
  await stadiumsStore.fetchStadiums()
})
</script>

<style scoped>
.team-section {
  background-color: rgba(26, 41, 66, 0.5);
  border-radius: 8px;
  padding: 16px;
}
</style>