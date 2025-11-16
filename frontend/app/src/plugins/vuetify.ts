import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import 'vuetify/styles'

// Champions League color scheme
const championsLeagueTheme = {
  dark: true,
  colors: {
    primary: '#001E40', // Deep navy blue
    secondary: '#00B2E3', // Bright blue
    accent: '#FFD700', // Gold
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
    background: '#0A1628', // Very dark blue
    surface: '#1A2942', // Dark blue surface
    'surface-variant': '#8793BD',
    'on-surface': '#FFFFFF',
    'on-primary': '#FFFFFF',
    'on-secondary': '#000000',
  }
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'championsLeagueTheme',
    themes: {
      championsLeagueTheme,
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  defaults: {
    VBtn: {
      elevation: 0,
      rounded: 'lg',
    },
    VCard: {
      elevation: 2,
      rounded: 'lg',
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
  },
})