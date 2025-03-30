<template>
  <div class="container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body p-4">
            <h2 class="text-center mb-4">Register</h2>

            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="form.username"
                  required
                  autocomplete="username"
                >
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  required
                  autocomplete="email"
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
                  autocomplete="new-password"
                >
              </div>

              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  required
                  autocomplete="new-password"
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
                Register
              </button>
            </form>

            <div class="text-center mt-3">
              <p class="mb-0">
                Already have an account?
                <router-link to="/login">Login</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()

    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const loading = ref(false)
    const error = ref('')

    const isFormValid = computed(() => {
      return (
        form.value.username &&
        form.value.email &&
        form.value.password &&
        form.value.password === form.value.confirmPassword
      )
    })

    const handleSubmit = async () => {
      if (!isFormValid.value) {
        error.value = 'Please fill in all fields and ensure passwords match'
        return
      }

      try {
        loading.value = true
        error.value = ''
        await store.dispatch('register', {
          username: form.value.username,
          email: form.value.email,
          password: form.value.password
        })
        router.push('/dashboard')
      } catch (err) {
        error.value = err.response?.data?.message || 'An error occurred during registration'
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
