<template>
  <div class="container py-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="vehicle" class="vehicle-detail">
      <!-- Header Section -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ vehicle.make }} {{ vehicle.model }} ({{ vehicle.year }})</h1>
        <div class="btn-group">
          <router-link :to="{ name: 'VehicleEdit', params: { id: vehicle.id }}" class="btn btn-primary">
            <i class="bi bi-pencil"></i> Edit Vehicle
          </router-link>
          <button @click="showDeleteModal = true" class="btn btn-danger">
            <i class="bi bi-trash"></i> Delete
          </button>
        </div>
      </div>

      <!-- Vehicle Details -->
      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Vehicle Information</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-sm-6">
                  <p><strong>VIN:</strong> {{ vehicle.vin }}</p>
                  <p><strong>License Plate:</strong> {{ vehicle.license_plate }}</p>
                  <p><strong>Gas Tank Size:</strong> {{ convertVolume(vehicle.gas_tank_size) }} {{ getVolumeUnit() }}</p>
                </div>
                <div class="col-sm-6">
                  <p><strong>Oil Capacity:</strong> {{ vehicle.oil_capacity }} quarts</p>
                  <p><strong>Transmission Fluid:</strong> {{ vehicle.transmission_fluid_capacity }} quarts</p>
                  <p><strong>Coolant Capacity:</strong> {{ vehicle.coolant_capacity }} quarts</p>
                  <p><strong>Brake Fluid Capacity:</strong> {{ vehicle.brake_fluid_capacity }} quarts</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fuel Records -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Fuel Records</h5>
              <router-link :to="{ name: 'FuelRecordCreate', params: { id: vehicle.id }}" class="btn btn-sm btn-success">
                <i class="bi bi-plus"></i> Add Fuel Record
              </router-link>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Mileage</th>
                      <th>Gallons</th>
                      <th>Cost</th>
                      <th>MPG</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="record in vehicle.fuel_records" :key="record.id">
                      <td>{{ formatDate(record.date) }}</td>
                      <td>{{ convertDistance(record.mileage) }} {{ getDistanceUnit() }}</td>
                      <td>{{ convertVolume(record.gallons) }} {{ getVolumeUnit() }}</td>
                      <td>{{ formatCurrency(record.total_cost) }}</td>
                      <td>{{ calculateMPG(record) }} {{ getDistanceUnit() }}/{{ getVolumeUnit() }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button 
                            class="btn btn-primary"
                            @click="handleEditFuelRecord(record)"
                            title="Edit Record"
                          >
                            <i class="bi bi-pencil-fill" />
                          </button>
                          <button 
                            class="btn btn-danger"
                            @click="handleDeleteFuelRecord(record)"
                            title="Delete Record"
                          >
                            <i class="bi bi-trash-fill" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Service Records -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Service Records</h5>
              <router-link :to="{ name: 'ServiceRecordCreate', params: { id: vehicle.id }}" class="btn btn-sm btn-success">
                <i class="bi bi-plus"></i> Add Service Record
              </router-link>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Type</th>
                      <th>Mileage</th>
                      <th>Cost</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="record in vehicle.service_records" :key="record.id">
                      <td>{{ formatDate(record.date) }}</td>
                      <td>{{ record.service_type }}</td>
                      <td>{{ record.mileage }}</td>
                      <td>${{ record.cost }}</td>
                      <td>{{ record.description }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button 
                            class="btn btn-primary"
                            @click="handleEditServiceRecord(record)"
                            title="Edit Record"
                          >
                            <i class="bi bi-pencil-fill" />
                          </button>
                          <button 
                            class="btn btn-danger"
                            @click="handleDeleteServiceRecord(record)"
                            title="Delete Record"
                          >
                            <i class="bi bi-trash-fill" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Timeline -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Timeline</h5>
              <router-link :to="{ name: 'Timeline', params: { id: vehicle.id }}" class="btn btn-sm btn-primary">
                View Full Timeline
              </router-link>
            </div>
            <div class="card-body">
              <div class="timeline-preview">
                <div v-for="event in timeline" :key="event.id" class="timeline-item">
                  <div class="timeline-date">{{ formatDate(event.date) }}</div>
                  <div class="timeline-content" :class="event.type">
                    <div class="timeline-header">
                      <span class="timeline-type">{{ event.type === 'fuel' ? 'Fuel Record' : 'Service Record' }}</span>
                      <span class="timeline-mileage">{{ convertDistance(event.data.mileage) }} {{ getDistanceUnit() }}</span>
                    </div>
                    <div class="timeline-details">
                      <template v-if="event.type === 'fuel'">
                        <div class="fuel-details">
                          <div class="detail-item">
                            <span class="label">Volume:</span>
                            <span class="value">{{ convertVolume(event.data.gallons) }} {{ getVolumeUnit() }}</span>
                          </div>
                          <div class="detail-item">
                            <span class="label">Cost:</span>
                            <span class="value">{{ formatCurrency(event.data.total_cost) }}</span>
                          </div>
                        </div>
                      </template>
                      <template v-else>
                        <div class="service-details">
                          <div class="detail-item">
                            <span class="label">Service Type:</span>
                            <span class="value">{{ event.data.service_type }}</span>
                          </div>
                          <div class="detail-item">
                            <span class="label">Cost:</span>
                            <span class="value">${{ event.data.cost }}</span>
                          </div>
                        </div>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal fade show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Vehicle</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this vehicle? This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Cancel</button>
            <button type="button" class="btn btn-danger" @click="handleDelete" :disabled="deleting">
              <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Fuel Record Modal -->
    <div v-if="editingFuelRecord" class="modal fade show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Fuel Record</h5>
            <button type="button" class="btn-close" @click="closeEditFuelModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleEditFuelSubmit">
              <div class="mb-3">
                <label class="form-label">Date & Time</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  v-model="editFuelForm.date"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Mileage</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editFuelForm.mileage"
                  required
                  min="0"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Gallons</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editFuelForm.gallons"
                  required
                  step="0.01"
                  min="0"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Cost per Gallon</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editFuelForm.cost_per_gallon"
                  required
                  step="0.01"
                  min="0"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea
                  class="form-control"
                  v-model="editFuelForm.notes"
                  rows="2"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditFuelModal">
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="handleEditFuelSubmit">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Service Record Modal -->
    <div v-if="editingServiceRecord" class="modal fade show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Service Record</h5>
            <button type="button" class="btn-close" @click="closeEditServiceModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleEditServiceSubmit">
              <div class="mb-3">
                <label class="form-label">Date & Time</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  v-model="editServiceForm.date"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Mileage</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editServiceForm.mileage"
                  required
                  min="0"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Service Type</label>
                <select class="form-select" v-model="editServiceForm.service_type" required>
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
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  class="form-control"
                  v-model="editServiceForm.description"
                  required
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Cost</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editServiceForm.cost"
                  required
                  step="0.01"
                  min="0"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea
                  class="form-control"
                  v-model="editServiceForm.notes"
                  rows="2"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditServiceModal">
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="handleEditServiceSubmit">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="editingFuelRecord || editingServiceRecord" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { 
  convertVolume, 
  convertDistance, 
  getVolumeUnit, 
  getDistanceUnit,
  formatCurrency,
  formatDate
} from '@/utils/unitConversions'

export default {
  name: 'VehicleDetail',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()

    const loading = ref(true)
    const showDeleteModal = ref(false)
    const deleting = ref(false)
    const editingFuelRecord = ref(null)
    const editingServiceRecord = ref(null)
    const editFuelForm = ref({})
    const editServiceForm = ref({})

    const vehicle = computed(() => store.getters.currentVehicle)

    const timeline = computed(() => {
      if (!vehicle.value) return []
      
      const events = []
      
      // Add fuel records
      vehicle.value.fuel_records.forEach(record => {
        events.push({
          id: `fuel-${record.id}`,
          type: 'fuel',
          date: record.date,
          data: record
        })
      })
      
      // Add service records
      vehicle.value.service_records.forEach(record => {
        events.push({
          id: `service-${record.id}`,
          type: 'service',
          date: record.date,
          data: record
        })
      })
      
      // Sort by date and limit to 5 most recent events
      return events.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 5)
    })

    const calculateMPG = (record) => {
      const previousRecord = vehicle.value.fuel_records
        .filter(r => r.mileage < record.mileage)
        .sort((a, b) => b.mileage - a.mileage)[0]

      if (!previousRecord) return '-'

      const miles = record.mileage - previousRecord.mileage
      const gallons = record.gallons
      return (miles / gallons).toFixed(1)
    }

    const handleDelete = async () => {
      try {
        deleting.value = true
        await store.dispatch('deleteVehicle', vehicle.value.id)
        router.push({ name: 'VehicleList' })
      } catch (error) {
        console.error('Error deleting vehicle:', error)
      } finally {
        deleting.value = false
        showDeleteModal.value = false
      }
    }

    const handleEditFuelRecord = (record) => {
      editingFuelRecord.value = record
      editFuelForm.value = { 
        ...record,
        date: new Date(record.date).toISOString().slice(0, 16)
      }
    }

    const closeEditFuelModal = () => {
      editingFuelRecord.value = null
      editFuelForm.value = {}
    }

    const handleEditFuelSubmit = async () => {
      try {
        await store.dispatch('updateFuelRecord', {
          vehicleId: vehicle.value.id,
          recordId: editingFuelRecord.value.id,
          data: editFuelForm.value
        })
        closeEditFuelModal()
      } catch (error) {
        console.error('Error updating fuel record:', error)
      }
    }

    const handleDeleteFuelRecord = async (record) => {
      if (!confirm('Are you sure you want to delete this fuel record?')) return

      try {
        await store.dispatch('deleteFuelRecord', {
          vehicleId: vehicle.value.id,
          recordId: record.id
        })
      } catch (error) {
        console.error('Error deleting fuel record:', error)
      }
    }

    const handleEditServiceRecord = (record) => {
      editingServiceRecord.value = record
      editServiceForm.value = { 
        ...record,
        date: new Date(record.date).toISOString().slice(0, 16)
      }
    }

    const closeEditServiceModal = () => {
      editingServiceRecord.value = null
      editServiceForm.value = {}
    }

    const handleEditServiceSubmit = async () => {
      try {
        await store.dispatch('updateServiceRecord', {
          vehicleId: vehicle.value.id,
          recordId: editingServiceRecord.value.id,
          data: editServiceForm.value
        })
        closeEditServiceModal()
      } catch (error) {
        console.error('Error updating service record:', error)
      }
    }

    const handleDeleteServiceRecord = async (record) => {
      if (!confirm('Are you sure you want to delete this service record?')) return

      try {
        await store.dispatch('deleteServiceRecord', {
          vehicleId: vehicle.value.id,
          recordId: record.id
        })
      } catch (error) {
        console.error('Error deleting service record:', error)
      }
    }

    onMounted(async () => {
      try {
        await store.dispatch('fetchVehicle', route.params.id)
      } catch (error) {
        console.error('Error fetching vehicle:', error)
        router.push({ name: 'VehicleList' })
      } finally {
        loading.value = false
      }
    })

    return {
      vehicle,
      loading,
      showDeleteModal,
      deleting,
      timeline,
      formatDate,
      calculateMPG,
      handleDelete,
      editingFuelRecord,
      editingServiceRecord,
      editFuelForm,
      editServiceForm,
      handleEditFuelRecord,
      closeEditFuelModal,
      handleEditFuelSubmit,
      handleDeleteFuelRecord,
      handleEditServiceRecord,
      closeEditServiceModal,
      handleEditServiceSubmit,
      handleDeleteServiceRecord,
      convertVolume,
      convertDistance,
      getVolumeUnit,
      getDistanceUnit,
      formatCurrency
    }
  }
}
</script>

<style lang="scss" scoped>
.vehicle-detail {
  h1 {
    font-size: 2rem;
    margin-bottom: 0;
  }
}

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

.table {
  margin-bottom: 0;

  th {
    font-weight: 600;
    color: #495057;
  }

  td {
    vertical-align: middle;
  }
}

.timeline-preview {
  .timeline-item {
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 1rem;

    &:last-child {
      margin-bottom: 0;
    }

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0.25rem;
      width: 0.5rem;
      height: 0.5rem;
      border-radius: 50%;
      background: #6c757d;
    }
  }

  .timeline-date {
    font-size: 0.875rem;
    color: #6c757d;
    margin-bottom: 0.25rem;
  }

  .timeline-content {
    background: #f8f9fa;
    padding: 0.75rem;
    border-radius: 0.5rem;
    border-left: 4px solid #6c757d;

    &.fuel {
      border-left-color: #28a745;
    }

    &.service {
      border-left-color: #17a2b8;
    }
  }

  .timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .timeline-type {
    font-weight: 600;
    font-size: 0.875rem;

    .fuel & {
      color: #28a745;
    }

    .service & {
      color: #17a2b8;
    }
  }

  .timeline-mileage {
    font-size: 0.75rem;
    color: #6c757d;
  }

  .timeline-details {
    font-size: 0.75rem;
  }

  .detail-item {
    display: flex;
    margin-bottom: 0.25rem;

    &:last-child {
      margin-bottom: 0;
    }

    .label {
      font-weight: 500;
      margin-right: 0.5rem;
      color: #495057;
    }

    .value {
      color: #6c757d;
    }
  }
}

.btn-group-sm > .btn {
  padding: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s ease-in-out;
  border: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: translateY(0);
  }

  &.btn-primary {
    background-color: #0d6efd;
    &:hover {
      background-color: #0b5ed7;
    }
  }

  &.btn-danger {
    background-color: #dc3545;
    &:hover {
      background-color: #bb2d3b;
    }
  }

  i {
    font-size: 0.75rem;
  }
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  margin-top: 50px;
}
</style>
