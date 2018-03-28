<template>
  <div class="menu mt-3">

    <div class="container">
      <nav class="nav nav-pills justify-content-end">
        <router-link :to="{name: 'Buurten'}"
                     v-if="$route.name !== 'Buurten'"
                     class="nav-link">
                          <span class="linklabel">
                            Buurten
                          </span>
        </router-link>

        <a href="javascript:void(0)"
           v-if="!token" @click="login()"
           class="nav-link pr-0">
          Login
        </a>

        <a href="javascript:void(0)"
           v-if="token" @click="logout()"
           class="nav-link pr-0">
          Logout
        </a>
      </nav>
    </div>
  </div>

</template>

<script>
import { mapActions } from 'vuex'
import { authorize, logout, getToken } from '../services/auth'

export default {
  created () {
    this.token = getToken()
    this.setToken(this.token)
  },

  data () {
    return {
      token: null
    }
  },

  methods: {
    ...mapActions({
      setToken: 'setToken'
    }),

    login: function () {
      authorize()
    },

    logout: function () {
      logout()
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~stijl/scss/ams-colorpalette";

.menu {
  background-color: $ams-lichtgrijs;
}
</style>
