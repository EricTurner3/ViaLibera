import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: null,
    vehicles: [],
    currentVehicle: null,
    token: localStorage.getItem('token') || null,
    settings: {
      liquidUnit: 'gallons',
      distanceUnit: 'miles',
      dateFormat: 'MM/DD/YYYY',
      timeFormat: '12h',
      currencyFormat: 'USD'
    }
  },

  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setVehicles(state, vehicles) {
      state.vehicles = vehicles
    },
    setCurrentVehicle(state, vehicle) {
      state.currentVehicle = vehicle
    },
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    clearAuth(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
    },
    updateSettings(state, settings) {
      state.settings = settings
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
    vehicles: (state) => state.vehicles,
    currentVehicle: (state) => state.currentVehicle,
    vehicleById: (state) => (id) => state.vehicles.find(v => v.id === id),
    vehicleFuelRecords: (state) => (id) => {
      const vehicle = state.vehicles.find(v => v.id === id)
      return vehicle ? vehicle.fuel_records : []
    },
    vehicleServiceRecords: (state) => (id) => {
      const vehicle = state.vehicles.find(v => v.id === id)
      return vehicle ? vehicle.service_records : []
    },
    getSettings: (state) => state.settings,
    formatDate: (state) => (dateString) => {
      const date = new Date(dateString)
      switch (state.settings.dateFormat) {
        case 'MM/DD/YYYY':
          return date.toLocaleDateString('en-US')
        case 'DD/MM/YYYY':
          return date.toLocaleDateString('en-GB')
        case 'YYYY-MM-DD':
          return date.toISOString().split('T')[0]
        default:
          return date.toLocaleDateString()
      }
    },
    formatTime: (state) => (dateString) => {
      const date = new Date(dateString)
      if (state.settings.timeFormat === '12h') {
        return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
      } else {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      }
    },
    formatVolume: (state) => (volume) => {
      if (state.settings.liquidUnit === 'gallons') {
        return `${volume} gallons`
      } else {
        return `${(volume * 3.78541).toFixed(2)} liters`
      }
    },
    formatDistance: (state) => (distance) => {
      if (state.settings.distanceUnit === 'miles') {
        return `${distance} miles`
      } else {
        return `${(distance * 1.60934).toFixed(1)} km`
      }
    },
    formatCurrency: (state) => (amount) => {
      switch (state.settings.currencyFormat) {
        case 'USD':
          return `$${amount.toFixed(2)}`
        case 'EUR':
          return `€${amount.toFixed(2)}`
        case 'GBP':
          return `£${amount.toFixed(2)}`
        default:
          return `$${amount.toFixed(2)}`
      }
    }
  },

  actions: {
    async login({ commit, dispatch }, credentials) {
      const response = await axios.post('http://localhost:8000/api/login/', credentials)
      const { access } = response.data
      commit('setToken', access)
      await dispatch('fetchUser')
    },

    async register({ dispatch }, userData) {
      await axios.post('http://localhost:8000/api/register/', userData)
      await dispatch('login', {
        username: userData.username,
        password: userData.password
      })
    },

    async fetchUser({ commit, state }) {
      try {
        const response = await axios.get('http://localhost:8000/api/users/me/', {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setUser', response.data)
      } catch (error) {
        commit('clearAuth')
        throw error
      }
    },

    async fetchVehicles({ commit, state }) {
      const response = await axios.get('http://localhost:8000/api/vehicles/', {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      commit('setVehicles', response.data)
    },

    async fetchVehicle({ commit, state }, id) {
      const response = await axios.get(`http://localhost:8000/api/vehicles/${id}/`, {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      commit('setCurrentVehicle', response.data)
    },

    async createVehicle({ commit, state }, vehicleData) {
      try {
        const response = await axios.post('http://localhost:8000/api/vehicles/', vehicleData, {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setVehicles', [...state.vehicles, response.data])
        return response.data
      } catch (error) {
        console.error('Error creating vehicle:', error)
        throw error
      }
    },

    async updateVehicle({ commit, state }, { id, data }) {
      const response = await axios.put(`http://localhost:8000/api/vehicles/${id}/`, data, {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      commit('setVehicles', state.vehicles.map(v => v.id === id ? response.data : v))
      commit('setCurrentVehicle', response.data)
      return response.data
    },

    async deleteVehicle({ commit, state }, id) {
      await axios.delete(`http://localhost:8000/api/vehicles/${id}/`, {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      commit('setVehicles', state.vehicles.filter(v => v.id !== id))
      if (state.currentVehicle?.id === id) {
        commit('setCurrentVehicle', null)
      }
    },

    async createFuelRecord({ commit, state }, { vehicleId, data }) {
      const response = await axios.post(`http://localhost:8000/api/vehicles/${vehicleId}/fuel-records/`, data, {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      const updatedVehicle = { ...state.currentVehicle }
      updatedVehicle.fuel_records.push(response.data)
      commit('setCurrentVehicle', updatedVehicle)
      commit('setVehicles', state.vehicles.map(v => v.id === vehicleId ? updatedVehicle : v))
      return response.data
    },

    async createServiceRecord({ commit, state }, { vehicleId, data }) {
      const response = await axios.post(`http://localhost:8000/api/vehicles/${vehicleId}/service-records/`, data, {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      const updatedVehicle = { ...state.currentVehicle }
      updatedVehicle.service_records.push(response.data)
      commit('setCurrentVehicle', updatedVehicle)
      commit('setVehicles', state.vehicles.map(v => v.id === vehicleId ? updatedVehicle : v))
      return response.data
    },

    async updateFuelRecord({ commit, state }, { vehicleId, recordId, data }) {
      try {
        const response = await axios.put(
          `http://localhost:8000/api/vehicles/${vehicleId}/fuel-records/${recordId}/`,
          data,
          {
            headers: { Authorization: `Bearer ${state.token}` }
          }
        )
        
        // Update the current vehicle's fuel records
        const updatedVehicle = {
          ...state.currentVehicle,
          fuel_records: state.currentVehicle.fuel_records.map(record =>
            record.id === recordId ? response.data : record
          )
        }
        commit('setCurrentVehicle', updatedVehicle)
        
        // Update the vehicle in the vehicles list
        const updatedVehicles = state.vehicles.map(vehicle =>
          vehicle.id === vehicleId ? updatedVehicle : vehicle
        )
        commit('setVehicles', updatedVehicles)
        
        return response.data
      } catch (error) {
        console.error('Error updating fuel record:', error)
        throw error
      }
    },

    async deleteFuelRecord({ commit, state }, { vehicleId, recordId }) {
      try {
        await axios.delete(
          `http://localhost:8000/api/vehicles/${vehicleId}/fuel-records/${recordId}/`,
          {
            headers: { Authorization: `Bearer ${state.token}` }
          }
        )
        
        // Update the current vehicle's fuel records
        const updatedVehicle = {
          ...state.currentVehicle,
          fuel_records: state.currentVehicle.fuel_records.filter(record => record.id !== recordId)
        }
        commit('setCurrentVehicle', updatedVehicle)
        
        // Update the vehicle in the vehicles list
        const updatedVehicles = state.vehicles.map(vehicle =>
          vehicle.id === vehicleId ? updatedVehicle : vehicle
        )
        commit('setVehicles', updatedVehicles)
      } catch (error) {
        console.error('Error deleting fuel record:', error)
        throw error
      }
    },

    async updateServiceRecord({ commit, state }, { vehicleId, recordId, data }) {
      try {
        const response = await axios.put(
          `http://localhost:8000/api/vehicles/${vehicleId}/service-records/${recordId}/`,
          data,
          {
            headers: { Authorization: `Bearer ${state.token}` }
          }
        )
        
        // Update the current vehicle's service records
        const updatedVehicle = {
          ...state.currentVehicle,
          service_records: state.currentVehicle.service_records.map(record =>
            record.id === recordId ? response.data : record
          )
        }
        commit('setCurrentVehicle', updatedVehicle)
        
        // Update the vehicle in the vehicles list
        const updatedVehicles = state.vehicles.map(vehicle =>
          vehicle.id === vehicleId ? updatedVehicle : vehicle
        )
        commit('setVehicles', updatedVehicles)
        
        return response.data
      } catch (error) {
        console.error('Error updating service record:', error)
        throw error
      }
    },

    async deleteServiceRecord({ commit, state }, { vehicleId, recordId }) {
      try {
        await axios.delete(
          `http://localhost:8000/api/vehicles/${vehicleId}/service-records/${recordId}/`,
          {
            headers: { Authorization: `Bearer ${state.token}` }
          }
        )
        
        // Update the current vehicle's service records
        const updatedVehicle = {
          ...state.currentVehicle,
          service_records: state.currentVehicle.service_records.filter(record => record.id !== recordId)
        }
        commit('setCurrentVehicle', updatedVehicle)
        
        // Update the vehicle in the vehicles list
        const updatedVehicles = state.vehicles.map(vehicle =>
          vehicle.id === vehicleId ? updatedVehicle : vehicle
        )
        commit('setVehicles', updatedVehicles)
      } catch (error) {
        console.error('Error deleting service record:', error)
        throw error
      }
    },

    logout({ commit }) {
      commit('clearAuth')
    }
  }
})
