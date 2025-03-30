<template>
  <div class="container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body p-4">
            <h2 class="text-center mb-4">Login</h2>

            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="username" class="form-label">Username or Email</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="form.username"
                  required
                  placeholder="Enter your username or email"
                >
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                  autocomplete="current-password"
                >
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                Login
              </button>
            </form>

            <div class="text-center mt-3">
              <p class="mb-0">
                Don't have an account?
                <router-link to="/register">Register</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()

    const form = ref({
      username: '',
      password: ''
    })

    const loading = ref(false)
    const error = ref('')

    const handleSubmit = async () => {
      try {
        loading.value = true
        error.value = ''
        await store.dispatch('login', {
          username: form.value.username,
          password: form.value.password
        })
        router.push({ name: 'Dashboard' })
      } catch (error) {
        console.error('Login failed:', error)
        error.value = error.response?.data?.error || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      handleSubmit
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  border: none;
  border-radius: 0.5rem;
}

.form-control {
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;

  &:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
  }
}

.btn {
  padding: 0.75rem 1rem;
  font-weight: 500;
}
</style>
