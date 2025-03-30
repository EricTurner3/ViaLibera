<template>
  <div>
    <h2 class="mb-4">{{ isEditing ? 'Edit Vehicle' : 'Add New Vehicle' }}</h2>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="make" class="form-label">Make</label>
              <input
                type="text"
                class="form-control"
                id="make"
                v-model="form.make"
                required
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="model" class="form-label">Model</label>
              <input
                type="text"
                class="form-control"
                id="model"
                v-model="form.model"
                required
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="year" class="form-label">Year</label>
              <input
                type="number"
                class="form-control"
                id="year"
                v-model="form.year"
                required
                min="1900"
                :max="new Date().getFullYear() + 1"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="vin" class="form-label">VIN</label>
              <input
                type="text"
                class="form-control"
                id="vin"
                v-model="form.vin"
                required
                pattern="[A-HJ-NPR-Z0-9]{17}"
                title="Please enter a valid 17-character VIN"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="license_plate" class="form-label">License Plate</label>
              <input
                type="text"
                class="form-control"
                id="license_plate"
                v-model="form.license_plate"
                required
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="gas_tank_size" class="form-label">Gas Tank Size (gallons)</label>
              <input
                type="number"
                class="form-control"
                id="gas_tank_size"
                v-model="form.gas_tank_size"
                required
                step="0.1"
                min="0"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="oil_capacity" class="form-label">Oil Capacity (quarts)</label>
              <input
                type="number"
                class="form-control"
                id="oil_capacity"
                v-model="form.oil_capacity"
                required
                step="0.1"
                min="0"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="transmission_fluid_capacity" class="form-label">Transmission Fluid Capacity (quarts)</label>
              <input
                type="number"
                class="form-control"
                id="transmission_fluid_capacity"
                v-model="form.transmission_fluid_capacity"
                step="0.1"
                min="0"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="coolant_capacity" class="form-label">Coolant Capacity (quarts)</label>
              <input
                type="number"
                class="form-control"
                id="coolant_capacity"
                v-model="form.coolant_capacity"
                step="0.1"
                min="0"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="brake_fluid_capacity" class="form-label">Brake Fluid Capacity (quarts)</label>
              <input
                type="number"
                class="form-control"
                id="brake_fluid_capacity"
                v-model="form.brake_fluid_capacity"
                step="0.1"
                min="0"
              >
            </div>
          </div>

          <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="goBack">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Saving...' : (isEditing ? 'Update Vehicle' : 'Add Vehicle') }}
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

export default {
  name: 'VehicleForm',
  setup () {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)

    const isEditing = computed(() => route.params.id !== undefined)

    const form = ref({
      make: '',
      model: '',
      year: new Date().getFullYear(),
      vin: '',
      license_plate: '',
      gas_tank_size: '',
      oil_capacity: '',
      transmission_fluid_capacity: '',
      coolant_capacity: '',
      brake_fluid_capacity: ''
    })

    const handleSubmit = async () => {
      try {
        loading.value = true
        if (isEditing.value) {
          await store.dispatch('updateVehicle', {
            id: route.params.id,
            data: form.value
          })
        } else {
          await store.dispatch('createVehicle', form.value)
        }
        router.push('/vehicles')
      } catch (error) {
        console.error('Failed to save vehicle:', error)
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    onMounted(async () => {
      if (isEditing.value) {
        try {
          const vehicle = await store.dispatch('fetchVehicle', route.params.id)
          form.value = { ...vehicle }
        } catch (error) {
          console.error('Failed to fetch vehicle:', error)
          router.push('/vehicles')
        }
      }
    })

    return {
      form,
      loading,
      isEditing,
      handleSubmit,
      goBack
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
}

.btn {
  padding: 0.5rem 1rem;
  font-weight: 500;
}
</style>
