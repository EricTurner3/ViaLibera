import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import VehicleList from '../views/vehicles/VehicleList.vue'
import VehicleDetail from '../views/vehicles/VehicleDetail.vue'
import VehicleForm from '../views/vehicles/VehicleForm.vue'
import FuelRecordForm from '../views/vehicles/FuelRecordForm.vue'
import ServiceRecordForm from '../views/vehicles/ServiceRecordForm.vue'
import Timeline from '../views/vehicles/Timeline.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles',
    name: 'VehicleList',
    component: VehicleList,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/new',
    name: 'VehicleCreate',
    component: VehicleForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/:id',
    name: 'VehicleDetail',
    component: VehicleDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/:id/edit',
    name: 'VehicleEdit',
    component: VehicleForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/:id/fuel/new',
    name: 'FuelRecordCreate',
    component: FuelRecordForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/:id/service/new',
    name: 'ServiceRecordCreate',
    component: ServiceRecordForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles/:id/timeline',
    name: 'Timeline',
    component: Timeline,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
