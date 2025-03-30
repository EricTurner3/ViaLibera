<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>My Vehicles</h2>
      <router-link to="/vehicles/new" class="btn btn-primary">
        Add New Vehicle
      </router-link>
    </div>

    <div class="row">
      <div v-for="vehicle in vehicles" :key="vehicle.id" class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ vehicle.year }} {{ vehicle.make }} {{ vehicle.model }}</h5>
            <p class="card-text">
              <strong>VIN:</strong> {{ vehicle.vin }}<br>
              <strong>License Plate:</strong> {{ vehicle.license_plate }}<br>
              <strong>Gas Tank Size:</strong> {{ vehicle.gas_tank_size }} gallons<br>
              <strong>Oil Capacity:</strong> {{ vehicle.oil_capacity }} quarts
            </p>
            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group">
                <router-link :to="'/vehicles/' + vehicle.id" class="btn btn-outline-primary">
                  View Details
                </router-link>
                <router-link :to="'/vehicles/' + vehicle.id + '/edit'" class="btn btn-outline-secondary">
                  Edit
                </router-link>
                <button @click="confirmDelete(vehicle)" class="btn btn-outline-danger">
                  Delete
                </button>
              </div>
              <small class="text-muted">
                Added {{ formatDate(vehicle.created_at) }}
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this vehicle? This action cannot be undone.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteVehicle">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useStore } from 'vuex'
import { Modal } from 'bootstrap'

export default {
  name: 'VehicleList',
  setup () {
    const store = useStore()
    const deleteModal = ref(null)
    const vehicleToDelete = ref(null)

    const vehicles = computed(() => store.getters.vehicles)

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const confirmDelete = (vehicle) => {
      vehicleToDelete.value = vehicle
      deleteModal.value.show()
    }

    const deleteVehicle = async () => {
      if (!vehicleToDelete.value) return

      try {
        await store.dispatch('deleteVehicle', vehicleToDelete.value.id)
        deleteModal.value.hide()
      } catch (error) {
        console.error('Failed to delete vehicle:', error)
      }
    }

    onMounted(async () => {
      await store.dispatch('fetchVehicles')
      deleteModal.value = new Modal(document.getElementById('deleteModal'))
    })

    return {
      vehicles,
      formatDate,
      confirmDelete,
      deleteVehicle
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
}

.card-title {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.card-text {
  color: #6c757d;
  margin-bottom: 1rem;
}

.btn-group {
  .btn {
    padding: 0.375rem 0.75rem;
  }
}

.modal-content {
  border-radius: 0.5rem;
  border: none;
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}
</style>
