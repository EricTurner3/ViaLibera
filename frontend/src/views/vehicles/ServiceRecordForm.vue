<template>
  <div>
    <h2 class="mb-4">Add Service Record</h2>

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
              <label for="service_type" class="form-label">Service Type</label>
              <select
                class="form-select"
                id="service_type"
                v-model="form.service_type"
                required
              >
                <option value="">Select a service type</option>
                <option value="Oil Change">Oil Change</option>
                <option value="Tire Rotation">Tire Rotation</option>
                <option value="Brake Service">Brake Service</option>
                <option value="Transmission Service">Transmission Service</option>
                <option value="Coolant Flush">Coolant Flush</option>
                <option value="Air Filter">Air Filter</option>
                <option value="Battery">Battery</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="mileage" class="form-label">Current Mileage</label>
              <input
                type="number"
                class="form-control"
                id="mileage"
                v-model="form.mileage"
                required
                min="0"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea
                class="form-control"
                id="description"
                v-model="form.description"
                rows="3"
                required
              ></textarea>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="cost" class="form-label">Cost</label>
              <input
                type="number"
                class="form-control"
                id="cost"
                v-model="form.cost"
                required
                step="0.01"
                min="0"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea
                class="form-control"
                id="notes"
                v-model="form.notes"
                rows="1"
              ></textarea>
            </div>
          </div>

          <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="goBack">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Saving...' : 'Add Service Record' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ServiceRecordForm',
  setup () {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)

    const form = ref({
      date: new Date().toISOString().slice(0, 16),
      service_type: '',
      mileage: '',
      description: '',
      cost: '',
      notes: ''
    })

    const handleSubmit = async () => {
      try {
        loading.value = true
        await store.dispatch('createServiceRecord', {
          vehicleId: route.params.id,
          data: form.value
        })
        router.push(`/vehicles/${route.params.id}`)
      } catch (error) {
        console.error('Failed to save service record:', error)
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
      form,
      loading,
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

.form-control,
.form-select {
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
