<template>
  <div id="app">
    <Navigation />
    <div class="container mt-4">
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Navigation from './components/Navigation.vue'

export default {
  name: 'App',
  components: {
    Navigation
  },
  setup () {
    const store = useStore()
    const error = computed(() => store.getters.error)

    return {
      error
    }
  }
}
</script>

<style lang="scss">
@import 'bootstrap/dist/css/bootstrap.min.css';

#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar {
  margin-bottom: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.alert {
  margin-bottom: 1rem;
}
</style>
