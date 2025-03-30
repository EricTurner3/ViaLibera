<template>
  <div class="container py-4">
    <h1 class="mb-4">Settings</h1>
    
    <div class="row">
      <div class="col-md-8">
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="card-title mb-0">Unit Preferences</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="saveSettings">
              <div class="mb-3">
                <label class="form-label">Liquid Volume Unit</label>
                <select class="form-select" v-model="settings.liquidUnit">
                  <option value="gallons">Gallons (Imperial)</option>
                  <option value="liters">Liters (Metric)</option>
                </select>
                <div class="form-text">This will affect how fuel records are displayed and entered.</div>
              </div>

              <div class="mb-3">
                <label class="form-label">Distance Unit</label>
                <select class="form-select" v-model="settings.distanceUnit">
                  <option value="miles">Miles (Imperial)</option>
                  <option value="kilometers">Kilometers (Metric)</option>
                </select>
                <div class="form-text">This will affect how mileage and distances are displayed.</div>
              </div>

              <div class="mb-3">
                <label class="form-label">Date Format</label>
                <select class="form-select" v-model="settings.dateFormat">
                  <option value="MM/DD/YYYY">MM/DD/YYYY (US)</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY (UK/EU)</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD (ISO)</option>
                </select>
                <div class="form-text">This will affect how dates are displayed throughout the application.</div>
              </div>

              <div class="mb-3">
                <label class="form-label">Time Format</label>
                <select class="form-select" v-model="settings.timeFormat">
                  <option value="12h">12-hour (AM/PM)</option>
                  <option value="24h">24-hour</option>
                </select>
                <div class="form-text">This will affect how times are displayed throughout the application.</div>
              </div>

              <div class="mb-3">
                <label class="form-label">Currency Format</label>
                <select class="form-select" v-model="settings.currencyFormat">
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="GBP">GBP (£)</option>
                </select>
                <div class="form-text">This will affect how monetary values are displayed.</div>
              </div>

              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary">
                  Save Settings
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Preview</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <h6>Date & Time</h6>
              <p class="mb-1">{{ formatPreviewDate }}</p>
              <p class="mb-1">{{ formatPreviewTime }}</p>
            </div>
            <div class="mb-3">
              <h6>Fuel Record</h6>
              <p class="mb-1">Volume: {{ formatPreviewVolume }}</p>
              <p class="mb-1">Distance: {{ formatPreviewDistance }}</p>
              <p class="mb-1">Cost: {{ formatPreviewCost }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Settings',
  setup() {
    const store = useStore()
    const settings = ref({
      liquidUnit: 'gallons',
      distanceUnit: 'miles',
      dateFormat: 'MM/DD/YYYY',
      timeFormat: '12h',
      currencyFormat: 'USD'
    })

    // Load saved settings on mount
    onMounted(() => {
      const savedSettings = localStorage.getItem('appSettings')
      if (savedSettings) {
        settings.value = JSON.parse(savedSettings)
      }
    })

    // Save settings to localStorage and Vuex
    const saveSettings = () => {
      localStorage.setItem('appSettings', JSON.stringify(settings.value))
      store.commit('updateSettings', settings.value)
    }

    // Preview formatting
    const formatPreviewDate = computed(() => {
      const date = new Date()
      switch (settings.value.dateFormat) {
        case 'MM/DD/YYYY':
          return date.toLocaleDateString('en-US')
        case 'DD/MM/YYYY':
          return date.toLocaleDateString('en-GB')
        case 'YYYY-MM-DD':
          return date.toISOString().split('T')[0]
        default:
          return date.toLocaleDateString()
      }
    })

    const formatPreviewTime = computed(() => {
      const date = new Date()
      if (settings.value.timeFormat === '12h') {
        return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
      } else {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      }
    })

    const formatPreviewVolume = computed(() => {
      const volume = 10
      return settings.value.liquidUnit === 'gallons' 
        ? `${volume} gallons`
        : `${(volume * 3.78541).toFixed(2)} liters`
    })

    const formatPreviewDistance = computed(() => {
      const distance = 100
      return settings.value.distanceUnit === 'miles'
        ? `${distance} miles`
        : `${(distance * 1.60934).toFixed(1)} km`
    })

    const formatPreviewCost = computed(() => {
      const cost = 50
      switch (settings.value.currencyFormat) {
        case 'USD':
          return `$${cost.toFixed(2)}`
        case 'EUR':
          return `€${cost.toFixed(2)}`
        case 'GBP':
          return `£${cost.toFixed(2)}`
        default:
          return `$${cost.toFixed(2)}`
      }
    })

    return {
      settings,
      saveSettings,
      formatPreviewDate,
      formatPreviewTime,
      formatPreviewVolume,
      formatPreviewDistance,
      formatPreviewCost
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
  border-radius: 0.5rem;

  .card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    padding: 1rem;
  }

  .card-title {
    font-size: 1.25rem;
    font-weight: 600;
  }
}

.form-select {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
  padding: 0.5rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #212529;
  background-color: #fff;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;

  &:focus {
    border-color: #86b7fe;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  }
}

.form-text {
  font-size: 0.875rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

h6 {
  color: #495057;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
</style> 