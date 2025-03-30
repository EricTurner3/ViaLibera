<template>
  <div class="container py-4">
    <h1 class="mb-4">Dashboard</h1>

    <div class="row">
      <!-- Vehicle Summary -->
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Vehicle Summary</h5>
            <router-link to="/vehicles" class="btn btn-sm btn-primary">View All</router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="vehicles.length === 0" class="text-center text-muted">
              <p>No vehicles found. Add your first vehicle to get started!</p>
              <router-link to="/vehicles/new" class="btn btn-primary">Add Vehicle</router-link>
            </div>
            <div v-else>
              <div v-for="vehicle in vehicles" :key="vehicle.id" class="vehicle-summary mb-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">{{ vehicle.make }} {{ vehicle.model }}</h6>
                    <p class="mb-0 text-muted small">{{ vehicle.year }} • {{ vehicle.license_plate }}</p>
                  </div>
                  <router-link :to="{ name: 'VehicleDetail', params: { id: vehicle.id }}" class="btn btn-sm btn-outline-primary">
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-header">
            <h5 class="card-title mb-0">Recent Activity</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="recentActivity.length === 0" class="text-center text-muted">
              <p>No recent activity to display.</p>
            </div>
            <div v-else class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon" :class="activity.type">
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-details">
                    <span class="vehicle-name">{{ activity.vehicle }}</span>
                    <span class="activity-date">{{ formatDate(activity.date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Maintenance Alerts -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Maintenance Alerts</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="maintenanceAlerts.length === 0" class="text-center text-muted">
              <p>No maintenance alerts at this time.</p>
            </div>
            <div v-else class="alert-list">
              <div v-for="alert in maintenanceAlerts" :key="alert.id" class="alert-item">
                <div class="alert-icon" :class="alert.severity">
                  <i :class="getAlertIcon(alert.severity)"></i>
                </div>
                <div class="alert-content">
                  <div class="alert-title">{{ alert.title }}</div>
                  <div class="alert-details">
                    <span class="vehicle-name">{{ alert.vehicle }}</span>
                    <span class="alert-date">Due: {{ formatDate(alert.dueDate) }}</span>
                  </div>
                  <div class="alert-description">{{ alert.description }}</div>
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

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const loading = ref(true)

    const vehicles = computed(() => store.getters.vehicles)

    const recentActivity = computed(() => {
      const activities = []
      vehicles.value.forEach(vehicle => {
        // Add fuel records
        vehicle.fuel_records.forEach(record => {
          activities.push({
            id: `fuel-${record.id}`,
            type: 'fuel',
            title: 'Fuel Record Added',
            vehicle: `${vehicle.make} ${vehicle.model}`,
            date: record.date
          })
        })

        // Add service records
        vehicle.service_records.forEach(record => {
          activities.push({
            id: `service-${record.id}`,
            type: 'service',
            title: 'Service Record Added',
            vehicle: `${vehicle.make} ${vehicle.model}`,
            date: record.date
          })
        })
      })

      return activities.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 5)
    })

    const maintenanceAlerts = computed(() => {
      const alerts = []
      vehicles.value.forEach(vehicle => {
        // Check for upcoming oil changes (every 5,000 miles)
        const lastOilChange = vehicle.service_records
          .filter(r => r.service_type === 'Oil Change')
          .sort((a, b) => new Date(b.date) - new Date(a.date))[0]

        if (lastOilChange) {
          const nextOilChange = lastOilChange.mileage + 5000
          if (nextOilChange - vehicle.current_mileage < 1000) {
            alerts.push({
              id: `oil-${vehicle.id}`,
              severity: 'warning',
              title: 'Oil Change Due Soon',
              vehicle: `${vehicle.make} ${vehicle.model}`,
              dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days from now
              description: `Next oil change due at ${nextOilChange} miles (${nextOilChange - vehicle.current_mileage} miles remaining)`
            })
          }
        }

        // Add more maintenance alerts as needed
      })

      return alerts.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate))
    })

    const getActivityIcon = (type) => {
      return {
        fuel: 'bi bi-fuel-pump',
        service: 'bi bi-tools'
      }[type]
    }

    const getAlertIcon = (severity) => {
      return {
        warning: 'bi bi-exclamation-triangle',
        danger: 'bi bi-exclamation-circle',
        info: 'bi bi-info-circle'
      }[severity]
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    onMounted(async () => {
      try {
        await store.dispatch('fetchVehicles')
      } catch (error) {
        console.error('Error fetching vehicles:', error)
      } finally {
        loading.value = false
      }
    })

    return {
      loading,
      vehicles,
      recentActivity,
      maintenanceAlerts,
      getActivityIcon,
      getAlertIcon,
      formatDate
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

.vehicle-summary {
  padding: 0.75rem;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
  transition: background-color 0.2s;

  &:hover {
    background-color: #e9ecef;
  }

  h6 {
    margin: 0;
    font-weight: 600;
  }
}

.activity-list {
  .activity-item {
    display: flex;
    align-items: flex-start;
    padding: 0.75rem 0;
    border-bottom: 1px solid #dee2e6;

    &:last-child {
      border-bottom: none;
    }
  }

  .activity-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    flex-shrink: 0;

    &.fuel {
      background-color: #d4edda;
      color: #155724;
    }

    &.service {
      background-color: #cce5ff;
      color: #004085;
    }

    i {
      font-size: 1rem;
    }
  }

  .activity-content {
    flex-grow: 1;
  }

  .activity-title {
    font-weight: 500;
    margin-bottom: 0.25rem;
  }

  .activity-details {
    font-size: 0.875rem;
    color: #6c757d;

    .vehicle-name {
      margin-right: 0.5rem;
    }
  }
}

.alert-list {
  .alert-item {
    display: flex;
    align-items: flex-start;
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
    margin-bottom: 1rem;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .alert-icon {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    flex-shrink: 0;

    &.warning {
      background-color: #fff3cd;
      color: #856404;
    }

    &.danger {
      background-color: #f8d7da;
      color: #721c24;
    }

    &.info {
      background-color: #d1ecf1;
      color: #0c5460;
    }

    i {
      font-size: 1.25rem;
    }
  }

  .alert-content {
    flex-grow: 1;
  }

  .alert-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .alert-details {
    font-size: 0.875rem;
    color: #6c757d;
    margin-bottom: 0.5rem;

    .vehicle-name {
      margin-right: 0.5rem;
    }
  }

  .alert-description {
    font-size: 0.875rem;
    color: #495057;
  }
}
</style>
