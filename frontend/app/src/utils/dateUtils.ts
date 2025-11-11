/**
 * Utility functions for date formatting with UTC+2 timezone
 */

const UTC_PLUS_2_OFFSET = 2 * 60 // 2 hours in minutes

/**
 * Convert UTC date to UTC+2
 */
export function toUTCPlus2(date: Date): Date {
  const utcDate = new Date(date.getTime())
  utcDate.setMinutes(utcDate.getMinutes() + UTC_PLUS_2_OFFSET)
  return utcDate
}

/**
 * Convert UTC+2 date to UTC (for sending to backend)
 */
export function toUTC(date: Date): Date {
  const utcDate = new Date(date.getTime())
  utcDate.setMinutes(utcDate.getMinutes() - UTC_PLUS_2_OFFSET)
  return utcDate
}

/**
 * Format date string (UTC) to display format in UTC+2
 * Example: "2025-10-19T14:40:51.562Z" -> "19 Oct 2025"
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const utcPlus2 = toUTCPlus2(date)
  
  return utcPlus2.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

/**
 * Format date string (UTC) to full datetime format in UTC+2
 * Example: "2025-10-19T14:40:51.562Z" -> "Saturday, 19 October 2025, 16:40"
 */
export function formatDateTime(dateString: string): string {
  const date = new Date(dateString)
  const utcPlus2 = toUTCPlus2(date)
  
  return utcPlus2.toLocaleString('en-GB', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Format date string (UTC) to time only in UTC+2
 * Example: "2025-10-19T14:40:51.562Z" -> "16:40"
 */
export function formatTime(dateString: string): string {
  const date = new Date(dateString)
  const utcPlus2 = toUTCPlus2(date)
  
  return utcPlus2.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Get current datetime in UTC+2 as ISO string (for datetime-local input)
 * Returns format: "2025-10-19T16:40"
 */
export function getCurrentDateTimeLocalUTCPlus2(): string {
  const now = new Date()
  const utcPlus2 = toUTCPlus2(now)
  
  // Format for datetime-local input: YYYY-MM-DDTHH:mm
  const year = utcPlus2.getUTCFullYear()
  const month = String(utcPlus2.getUTCMonth() + 1).padStart(2, '0')
  const day = String(utcPlus2.getUTCDate()).padStart(2, '0')
  const hours = String(utcPlus2.getUTCHours()).padStart(2, '0')
  const minutes = String(utcPlus2.getUTCMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

/**
 * Convert datetime-local string (in UTC+2) to UTC ISO string for backend
 * Input: "2025-10-19T16:40" (assumed UTC+2)
 * Output: "2025-10-19T14:40:00.000Z" (UTC)
 */
export function dateTimeLocalToUTC(dateTimeLocal: string): string {
  // Parse as UTC first
  const date = new Date(dateTimeLocal + ':00.000Z')
  // Then subtract 2 hours to convert from UTC+2 to UTC
  const utc = toUTC(date)
  return utc.toISOString()
}

export function parseIsoToUtcPlus2(isoString: string) {
  // Ensure input is valid
  if (!isoString) throw new Error("ISO string required")

  // Some ISO strings (like yours) lack the 'Z' or offset — assume UTC
  const normalized = isoString.endsWith('Z') ? isoString : isoString + 'Z'

  // Parse as UTC
  const date = new Date(normalized)

  // Add +2 hours (in milliseconds)
  const utcPlus2 = new Date(date.getTime())

  return utcPlus2
}
