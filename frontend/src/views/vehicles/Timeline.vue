<template>
  <div class="container py-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="vehicle" class="timeline-view">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Vehicle History Timeline</h1>
        <router-link :to="{ name: 'VehicleDetail', params: { id: vehicle.id }}" class="btn btn-outline-primary">
          <i class="bi bi-arrow-left"></i> Back to Vehicle
        </router-link>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="timeline">
            <div v-for="event in timeline" :key="event.id" class="timeline-item">
              <div class="timeline-date">{{ formatDate(event.date) }}</div>
              <div class="timeline-content" :class="event.type">
                <div class="timeline-header">
                  <span class="timeline-type">{{ event.type === 'fuel' ? 'Fuel Record' : 'Service Record' }}</span>
                  <span class="timeline-mileage">{{ event.data.mileage }} miles</span>
                </div>
                <div class="timeline-details">
                  <template v-if="event.type === 'fuel'">
                    <div class="fuel-details">
                      <div class="detail-item">
                        <span class="label">Gallons:</span>
                        <span class="value">{{ event.data.gallons }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Cost/Gallon:</span>
                        <span class="value">${{ event.data.cost_per_gallon }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Total Cost:</span>
                        <span class="value">${{ event.data.total_cost }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">MPG:</span>
                        <span class="value">{{ calculateMPG(event.data) }}</span>
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
                      <div class="detail-item">
                        <span class="label">Description:</span>
                        <span class="value">{{ event.data.description }}</span>
                      </div>
                    </div>
                  </template>
                  <div v-if="event.data.notes" class="timeline-notes">
                    {{ event.data.notes }}
                  </div>
                </div>
              </div>
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
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Timeline',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()

    const loading = ref(true)
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
      
      // Sort by date
      return events.sort((a, b) => new Date(b.date) - new Date(a.date))
    })

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const calculateMPG = (record) => {
      const previousRecord = vehicle.value.fuel_records
        .filter(r => r.mileage < record.mileage)
        .sort((a, b) => b.mileage - a.mileage)[0]

      if (!previousRecord) return '-'

      const miles = record.mileage - previousRecord.mileage
      return (miles / record.gallons).toFixed(1)
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
      timeline,
      formatDate,
      calculateMPG
    }
  }
}
</script>

<style lang="scss" scoped>
.timeline-view {
  h1 {
    font-size: 2rem;
    margin-bottom: 0;
  }
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
  border-radius: 0.5rem;
}

.timeline {
  position: relative;
  padding: 1rem 0;

  &::before {
    content: '';
    position: absolute;
    left: 1rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #e9ecef;
  }
}

.timeline-item {
  position: relative;
  padding-left: 3rem;
  margin-bottom: 2rem;

  &:last-child {
    margin-bottom: 0;
  }

  &::before {
    content: '';
    position: absolute;
    left: 0.75rem;
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
  padding: 1rem;
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
  font-size: 1rem;

  .fuel & {
    color: #28a745;
  }

  .service & {
    color: #17a2b8;
  }
}

.timeline-mileage {
  font-size: 0.875rem;
  color: #6c757d;
}

.timeline-details {
  font-size: 0.875rem;
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

.timeline-notes {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #dee2e6;
  font-style: italic;
  color: #6c757d;
}
</style>
