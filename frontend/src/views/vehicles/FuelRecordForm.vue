<template>
  <div>
    <h2 class="mb-4">Add Fuel Record</h2>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="date" class="form-label">Date & Time</label>
              <input
                type="datetime-local"
                class="form-control"
                id="date"
                v-model="form.date"
                required
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="mileage" class="form-label">Current Mileage ({{ getDistanceUnit() }})</label>
              <input
                type="number"
                class="form-control"
                id="mileage"
                v-model="form.mileage"
                required
                min="0"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="gallons" class="form-label">Volume Added ({{ getVolumeUnit() }})</label>
              <input
                type="number"
                class="form-control"
                id="gallons"
                v-model="form.gallons"
                required
                step="0.01"
                min="0"
                :max="vehicle.gas_tank_size"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="cost_per_gallon" class="form-label">Cost per {{ getVolumeUnit() }}</label>
              <input
                type="number"
                class="form-control"
                id="cost_per_gallon"
                v-model="form.cost_per_gallon"
                required
                step="0.01"
                min="0"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="total_cost" class="form-label">Total Cost</label>
              <input
                type="text"
                class="form-control"
                id="total_cost"
                :value="formatCurrency(totalCost)"
                readonly
              >
            </div>
          </div>

          <div class="mb-3">
            <label for="notes" class="form-label">Notes</label>
            <textarea
              class="form-control"
              id="notes"
              v-model="form.notes"
              rows="3"
            ></textarea>
          </div>

          <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="goBack">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Saving...' : 'Add Fuel Record' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { 
  getVolumeUnit, 
  getDistanceUnit,
  formatCurrency
} from '@/utils/unitConversions'

export default {
  name: 'FuelRecordForm',
  setup () {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)

    const vehicle = computed(() => store.getters.currentVehicle)

    const form = ref({
      date: new Date().toISOString().slice(0, 16),
      mileage: '',
      gallons: '',
      cost_per_gallon: '',
      notes: ''
    })

    const totalCost = computed(() => {
      const gallons = parseFloat(form.value.gallons) || 0
      const costPerGallon = parseFloat(form.value.cost_per_gallon) || 0
      return (gallons * costPerGallon).toFixed(2)
    })

    const handleSubmit = async () => {
      try {
        loading.value = true
        // Convert values back to standard units before sending to API
        const gallons = parseFloat(form.value.gallons) || 0
        const costPerGallon = parseFloat(form.value.cost_per_gallon) || 0
        const mileage = parseInt(form.value.mileage) || 0

        await store.dispatch('createFuelRecord', {
          vehicleId: route.params.id,
          data: {
            date: form.value.date,
            mileage: mileage,
            gallons: gallons,
            cost_per_gallon: costPerGallon,
            notes: form.value.notes
          }
        })
        router.push(`/vehicles/${route.params.id}`)
      } catch (error) {
        console.error('Failed to save fuel record:', error)
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    onMounted(async () => {
      await store.dispatch('fetchVehicle', route.params.id)
    })

    return {
      vehicle,
      form,
      loading,
      totalCost,
      handleSubmit,
      goBack,
      getVolumeUnit,
      getDistanceUnit,
      formatCurrency
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
  border-radius: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #2c3e50;
}

.form-control {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;

  &:focus {
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }

  &[readonly] {
    background-color: #f8f9fa;
  }
}

.btn {
  padding: 0.5rem 1rem;
  font-weight: 500;
}
</style>
