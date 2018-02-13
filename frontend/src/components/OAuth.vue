<template>
  <div>
    <button class="btn btn-outline-primary" v-if="!token" v-on:click="login()">Login</button>
    <button class="btn btn-outline-primary" v-if="token"  v-on:click="logout()">Logout</button>
  </div>
</template>

<script>
import { authorize, logout, getToken } from '../services/auth'

export default {
  created () {
    this.token = getToken()
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
  }
}
</script>

<style scoped>
</style>
