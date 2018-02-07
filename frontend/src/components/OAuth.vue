<template>
  <div>
    <button class="btn" v-if="!token" v-on:click="login()">Login</button>
    <button class="btn" v-if="token"  v-on:click="logout()">Logout</button>
  </div>
</template>

<script>
import { authorize, logout, getToken } from '../services/auth'

export default {
  created () {
  },
  data () {
    return {
      token: null
    }
  },
  methods: {
    login: function () {
      authorize()
    },
    logout: function () {
      logout()
    }
  },
  mounted () {
    this.token = getToken()
  },
  watch: {
  }
}
</script>

<style scoped>
</style>
