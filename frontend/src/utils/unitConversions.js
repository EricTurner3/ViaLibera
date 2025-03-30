// Conversion constants
const GALLONS_TO_LITERS = 3.78541
const MILES_TO_KILOMETERS = 1.60934

// Get user settings from localStorage
const getUserSettings = () => {
  const settings = localStorage.getItem('appSettings')
  return settings ? JSON.parse(settings) : {
    liquidUnit: 'gallons',
    distanceUnit: 'miles',
    dateFormat: 'MM/DD/YYYY',
    timeFormat: '12h',
    currencyFormat: 'USD'
  }
}

// Convert volume from gallons to liters
export const convertVolume = (gallons) => {
  const settings = getUserSettings()
  // Convert to number and handle invalid values
  const gallonsNum = parseFloat(gallons)
  if (isNaN(gallonsNum)) return '0.00'
  
  if (settings.liquidUnit === 'liters') {
    return (gallonsNum * GALLONS_TO_LITERS).toFixed(2)
  }
  return gallonsNum.toFixed(2)
}

// Convert distance from miles to kilometers
export const convertDistance = (miles) => {
  const settings = getUserSettings()
  // Convert to number and handle invalid values
  const milesNum = parseFloat(miles)
  if (isNaN(milesNum)) return '0.0'
  
  if (settings.distanceUnit === 'kilometers') {
    return (milesNum * MILES_TO_KILOMETERS).toFixed(1)
  }
  return milesNum
}

// Get the appropriate unit label for volume
export const getVolumeUnit = () => {
  const settings = getUserSettings()
  return settings.liquidUnit === 'liters' ? 'L' : 'gal'
}

// Get the appropriate unit label for distance
export const getDistanceUnit = () => {
  const settings = getUserSettings()
  return settings.distanceUnit === 'kilometers' ? 'km' : 'mi'
}

// Format currency based on user preferences
export const formatCurrency = (amount) => {
  const settings = getUserSettings()
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: settings.currencyFormat
  })
  return formatter.format(amount)
}

// Format date based on user preferences
export const formatDate = (dateString) => {
  const settings = getUserSettings()
  const date = new Date(dateString)
  
  switch (settings.dateFormat) {
    case 'MM/DD/YYYY':
      return date.toLocaleDateString('en-US')
    case 'DD/MM/YYYY':
      return date.toLocaleDateString('en-GB')
    case 'YYYY-MM-DD':
      return date.toISOString().split('T')[0]
    default:
      return date.toLocaleDateString()
  }
}

// Format time based on user preferences
export const formatTime = (dateString) => {
  const settings = getUserSettings()
  const date = new Date(dateString)
  
  if (settings.timeFormat === '12h') {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit', 
      hour12: true 
    })
  } else {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      hour12: false 
    })
  }
} 