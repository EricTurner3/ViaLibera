<template>
  <div class="timeline">
    <div v-for="record in sortedRecords" :key="record.id" class="timeline-item">
      <div class="timeline-content">
        <div class="timeline-header">
          <div class="timeline-date">
            {{ formatDateTime(record.date) }}
          </div>
          <div class="timeline-actions">
            <button 
              class="btn btn-sm btn-outline-primary me-2"
              @click="handleEdit(record)"
            >
              Edit
            </button>
            <button 
              class="btn btn-sm btn-outline-danger"
              @click="handleDelete(record)"
            >
              Delete
            </button>
          </div>
        </div>
        <div class="timeline-details">
          <div v-if="record.type === 'fuel'" class="fuel-record">
            <h5>Fuel Record</h5>
            <p>Mileage: {{ record.mileage }}</p>
            <p>Gallons: {{ record.gallons }}</p>
            <p>Cost per Gallon: ${{ record.cost_per_gallon }}</p>
            <p>Total Cost: ${{ record.total_cost }}</p>
            <p v-if="record.notes" class="notes">{{ record.notes }}</p>
          </div>
          <div v-else class="service-record">
            <h5>{{ record.service_type }}</h5>
            <p>Mileage: {{ record.mileage }}</p>
            <p>Description: {{ record.description }}</p>
            <p>Cost: ${{ record.cost }}</p>
            <p v-if="record.notes" class="notes">{{ record.notes }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingRecord" class="modal fade show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Edit {{ editingRecord.type === 'fuel' ? 'Fuel' : 'Service' }} Record
            </h5>
            <button type="button" class="btn-close" @click="closeEditModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleEditSubmit">
              <div class="mb-3">
                <label class="form-label">Date & Time</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  v-model="editForm.date"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Mileage</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="editForm.mileage"
                  required
                  min="0"
                >
              </div>
              <template v-if="editingRecord.type === 'fuel'">
                <div class="mb-3">
                  <label class="form-label">Gallons</label>
                  <input
                    type="number"
                    class="form-control"
                    v-model="editForm.gallons"
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
                    v-model="editForm.cost_per_gallon"
                    required
                    step="0.01"
                    min="0"
                  >
                </div>
              </template>
              <template v-else>
                <div class="mb-3">
                  <label class="form-label">Service Type</label>
                  <select class="form-select" v-model="editForm.service_type" required>
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
                    v-model="editForm.description"
                    required
                    rows="3"
                  ></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Cost</label>
                  <input
                    type="number"
                    class="form-control"
                    v-model="editForm.cost"
                    required
                    step="0.01"
                    min="0"
                  >
                </div>
              </template>
              <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea
                  class="form-control"
                  v-model="editForm.notes"
                  rows="2"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditModal">
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="handleEditSubmit">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="editingRecord" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  props: {
    fuelRecords: {
      type: Array,
      required: true
    },
    serviceRecords: {
      type: Array,
      required: true
    },
    vehicleId: {
      type: [Number, String],
      required: true
    }
  },
  setup(props, { emit }) {
    const store = useStore()
    const editingRecord = ref(null)
    const editForm = ref({})

    const sortedRecords = computed(() => {
      const allRecords = [
        ...props.fuelRecords.map(record => ({
          ...record,
          type: 'fuel',
          datetime: new Date(record.date)
        })),
        ...props.serviceRecords.map(record => ({
          ...record,
          type: 'service',
          datetime: new Date(record.date)
        }))
      ]
      
      return allRecords.sort((a, b) => b.datetime - a.datetime)
    })

    const formatDateTime = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const handleEdit = (record) => {
      editingRecord.value = record
      editForm.value = { ...record }
    }

    const closeEditModal = () => {
      editingRecord.value = null
      editForm.value = {}
    }

    const handleEditSubmit = async () => {
      try {
        if (editingRecord.value.type === 'fuel') {
          await store.dispatch('updateFuelRecord', {
            vehicleId: props.vehicleId,
            recordId: editingRecord.value.id,
            data: editForm.value
          })
        } else {
          await store.dispatch('updateServiceRecord', {
            vehicleId: props.vehicleId,
            recordId: editingRecord.value.id,
            data: editForm.value
          })
        }
        closeEditModal()
        emit('record-updated')
      } catch (error) {
        console.error('Error updating record:', error)
      }
    }

    const handleDelete = async (record) => {
      if (!confirm('Are you sure you want to delete this record?')) return

      try {
        if (record.type === 'fuel') {
          await store.dispatch('deleteFuelRecord', {
            vehicleId: props.vehicleId,
            recordId: record.id
          })
        } else {
          await store.dispatch('deleteServiceRecord', {
            vehicleId: props.vehicleId,
            recordId: record.id
          })
        }
        emit('record-deleted')
      } catch (error) {
        console.error('Error deleting record:', error)
      }
    }

    return {
      sortedRecords,
      formatDateTime,
      editingRecord,
      editForm,
      handleEdit,
      closeEditModal,
      handleEditSubmit,
      handleDelete
    }
  }
}
</script>

<style scoped>
.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline-item {
  position: relative;
  padding: 20px 0;
  border-left: 2px solid #e9ecef;
  margin-left: 20px;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 20px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #007bff;
}

.timeline-content {
  margin-left: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.timeline-date {
  font-weight: 500;
  color: #495057;
}

.timeline-actions {
  display: flex;
  gap: 8px;
}

.timeline-details {
  margin-top: 10px;
}

.timeline-details h5 {
  margin-bottom: 10px;
  color: #212529;
}

.notes {
  font-style: italic;
  color: #6c757d;
  margin-top: 8px;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  margin-top: 50px;
}
</style> 