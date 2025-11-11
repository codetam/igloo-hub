<template>
    <v-card elevation="2" class="timeline-card">
        <v-card-text class="px-8 py-6">
            <div class="timeline-container">
                <!-- Team legends -->
                <div class="team-legends mb-8">
                    <v-chip size="small" class="mr-2"
                        :style="{ background: theme.current.value.colors.secondary, color: '#fff' }">
                        <v-icon start size="small">mdi-soccer</v-icon>
                        Team 1
                    </v-chip>
                    <v-chip size="small" :style="{ background: theme.current.value.colors.accent, color: '#000' }">
                        <v-icon start size="small">mdi-soccer</v-icon>
                        Team 2
                    </v-chip>
                </div>

                <!-- Timeline Line -->
                <div class="timeline-line" :style="{ background: timelineGradient }">
                    <!-- Start marker -->
                    <div class="timeline-marker start-marker">
                        <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                                <div v-bind="props" class="marker-dot start-dot">
                                    <v-icon size="small" color="white">mdi-whistle</v-icon>
                                </div>
                            </template>
                            <span v-if="startTime">Kick Off<br>{{ formatTime(startTime) }}</span>
                        </v-tooltip>
                        <div class="marker-label">0'</div>
                    </div>

                    <!-- Goal markers -->
                    <div v-for="goal in sortedGoals" :key="goal.id" class="timeline-marker goal-marker"
                        :style="{ left: calculatePosition(goal.minute) + '%' }">
                        <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                                <div v-bind="props" class="marker-dot goal-dot"
                                    :style="{ background: getTeamColor(goal.team) }">
                                    <v-icon size="small" color="white">mdi-soccer</v-icon>
                                </div>
                            </template>
                            <div class="goal-tooltip">
                                <div class="font-weight-bold mb-1">
                                    ⚽ {{ goal.scorer.name }}
                                    <v-chip size="x-small"
                                        :style="{ background: getTeamColor(goal.team), color: getTextColor(goal.team) }"
                                        class="ml-1">
                                        Team {{ goal.team }}
                                    </v-chip>
                                </div>
                                <div v-if="goal.assister" class="text-caption">
                                    🎯 Assist: {{ goal.assister.name }}
                                </div>
                                <div class="text-caption text-grey mt-1">
                                    {{ getMinuteLabel(goal.minute) }}
                                </div>
                            </div>
                        </v-tooltip>
                        <div class="marker-label">{{ getMinuteLabel(goal.minute) }}</div>
                    </div>

                    <!-- End marker (if game ended) -->
                    <div v-if="endTime" class="timeline-marker end-marker">
                        <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                                <div v-bind="props" class="marker-dot end-dot">
                                    <v-icon size="small" color="white">mdi-whistle</v-icon>
                                </div>
                            </template>
                            <span>Full Time<br>{{ formatTime(endTime) }}</span>
                        </v-tooltip>
                        <div class="marker-label">{{ totalMinutes }}'</div>
                    </div>

                    <!-- Live marker (if game is live) -->
                    <div v-else-if="isLive" class="timeline-marker live-marker">
                        <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                                <div v-bind="props" class="marker-dot live-dot">
                                    <v-icon size="small" color="white">mdi-clock</v-icon>
                                </div>
                            </template>
                            <span>Live<br>{{ formatTime(new Date().toISOString()) }}</span>
                        </v-tooltip>
                        <div class="marker-label">{{ currentMinute }}'</div>
                    </div>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useTheme } from 'vuetify'
import type { Goal } from '@/types'
import { parseIsoToUtcPlus2 } from '@/utils/dateUtils'

interface Props {
    goals: Goal[]
    startTime?: string
    endTime?: string
    isLive?: boolean
}

const props = defineProps<Props>()
const theme = useTheme()

const currentTime = ref(new Date().toISOString())
let interval: number | null = null

onMounted(() => {
    if (props.isLive) {
        interval = window.setInterval(() => {
            currentTime.value = new Date().toISOString()
        }, 10000)
    }
})

onUnmounted(() => {
    if (interval) clearInterval(interval)
})

const sortedGoals = computed(() => {
    return [...props.goals].sort((a, b) => {
        const timeA = new Date(a.minute || '').getTime()
        const timeB = new Date(b.minute || '').getTime()
        return timeA - timeB
    })
})

const totalMinutes = computed(() => {
    if (!props.startTime) return 0
    const end = props.endTime
        ? parseIsoToUtcPlus2(props.endTime)
        : parseIsoToUtcPlus2(currentTime.value)
    const start = parseIsoToUtcPlus2(props.startTime)
    return Math.floor((end.getTime() - start.getTime()) / 60000)
})

const currentMinute = computed(() => {
    if (!props.startTime) return 0
    const start = parseIsoToUtcPlus2(props.startTime)
    const now = new Date(currentTime.value)
    return Math.floor((now.getTime() - start.getTime()) / 60000)
})

const duration = computed(() => {
    if (!props.startTime) return null
    const mins = props.endTime ? totalMinutes.value : currentMinute.value
    return `${mins} min`
})

const timelineGradient = computed(() => {
    const colors = theme.current.value.colors
    return `linear-gradient(90deg, ${colors.success} 0%, ${colors.secondary} 50%, ${colors.accent} 100%)`
})

function calculatePosition(minute?: string): number {
    if (!minute || !props.startTime) return 0
    const start = parseIsoToUtcPlus2(props.startTime).getTime()
    const goalTime = parseIsoToUtcPlus2(minute).getTime()
    const end = props.endTime
        ? parseIsoToUtcPlus2(props.endTime).getTime()
        : parseIsoToUtcPlus2(currentTime.value).getTime()

    const totalDuration = end - start
    const goalPosition = goalTime - start
    return Math.max(0, Math.min(100, (goalPosition / totalDuration) * 100))
}

function getMinuteLabel(minute?: string): string {
    if (!minute || !props.startTime) return "0'"
    const start = parseIsoToUtcPlus2(props.startTime).getTime()
    const goalTime = parseIsoToUtcPlus2(minute).getTime()
    const mins = Math.floor((goalTime - start) / 60000)
    return `${mins}'`
}

function formatTime(datetime: string): string {
    return parseIsoToUtcPlus2(datetime).toLocaleTimeString('it-IT', {
        hour: '2-digit',
        minute: '2-digit'
    })
}

function getTeamColor(team: number): string {
    const colors = theme.current.value.colors
    return team === 1 ? colors.secondary : colors.accent
}

function getTextColor(team: number): string {
    const colors = theme.current.value.colors
    return team === 1 ? colors['on-secondary'] || '#000' : colors['on-accent'] || '#000'
}
</script>

<style scoped>
.timeline-card {
    overflow: visible;
}

.timeline-container {
    position: relative;
    padding: 30px 0;
}

.timeline-line {
    position: relative;
    height: 8px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 2;
}

.marker-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.marker-dot:hover {
    transform: scale(1.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.start-marker {
    left: 0;
}

.start-dot {
    background: #4CAF50;
}

.end-marker {
    left: 100%;
}

.end-dot {
    background: #FF5722;
}

.live-marker {
    left: 100%;
    animation: pulse 2s infinite;
}

.live-dot {
    background: #f44336;
}

@keyframes pulse {

    0%,
    100% {
        box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7);
    }

    50% {
        box-shadow: 0 0 0 10px rgba(244, 67, 54, 0);
    }
}

.goal-tooltip {
    text-align: center;
}

.marker-label {
    position: absolute;
    top: 50px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 12px;
    font-weight: 600;
    color: #666;
    white-space: nowrap;
}

.team-legends {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
}

/* Mobile responsiveness */
@media (max-width: 600px) {
    .timeline-container {
        padding: 25px 0;
    }

    .marker-dot {
        width: 32px;
        height: 32px;
    }

    .marker-label {
        font-size: 11px;
        top: 45px;
    }

    .timeline-line {
        height: 6px;
    }
}

@media (max-width: 400px) {
    .marker-label {
        font-size: 10px;
    }

    .marker-dot {
        width: 28px;
        height: 28px;
    }
}
</style>
