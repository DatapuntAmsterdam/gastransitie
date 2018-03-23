<template>

  <div>
    <div class="outer-wrapper">
      <div class="grid-wrapper wrapper_12 header-wrapper ">
        <div class="grid-container container_12 grid-header-logo ">
          <div class="grid-zone grid_12 z-logo ">
            <div class="grid-blok grid_9 type-logo sponsored">
              <div class="grid-element">
                <div class="grid-edge">
                  <div class="grid-inside">
                    <h1 class="sitelogo">
                      <a class="mainlogo" href="#">
                      <span class="logoset">
                        <img src="/static/logos/andreas.svg" class="screen-logo" alt="Gemeente Amsterdam"/>
                        <img src="/static/logos/andreas.png" class="alt-logo" alt="Gemeente Amsterdam"/>
                        <img src="/static/logos/andreas-print.png" class="print-logo" alt="Gemeente Amsterdam"/>
                      </span>

                        <span class="logotexts">
                        <span class="logotext red">Gemeente</span>
                        <span class="logotext red">Amsterdam</span>
                      </span>

                      </a>
                      <span class="subsitetitle">
                      <a href="#">
                        City Deal Aardgasloos
                      </a>
                    </span>

                    </h1>

                  </div>

                </div>
              </div>
            </div>

            <div class="grid-blok grid_3 type-nav-secundair ">
              <div class="grid-element">
                <div class="grid-edge">
                  <div class="grid-inside">

                  </div>

                </div>
              </div>
            </div>

            <div class="zone-clear clear"></div>
          </div>

          <div class="clear"></div>
        </div>

        <div class="grid-container container_12 grid-header-nav breakout-container">
          <div class="grid-zone grid_12 z-nav ">
            <div class="grid-blok grid_12 type-nav-primair ">
              <div class="grid-element">
                <div class="grid-edge">
                  <div class="grid-inside">
                    <nav>
                      <ul class="links horizontal right ">
                        <li class="" v-if="!token" @click="login()">
                          <a href="javascript:void(0)" class="">
                            <span class="linklabel">
                              Login
                            </span>
                          </a>
                        </li>

                        <li class="" v-if="token" @click="logout()">
                          <a href="javascript:void(0)" class="">
                            <span class="linklabel">
                              Logout
                            </span>
                          </a>
                        </li>
                      </ul>
                    </nav>

                  </div>

                </div>
              </div>
            </div>

            <div class="zone-clear clear"></div>
          </div>

          <div class="clear"></div>
        </div>

      </div>
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

<style>
  .mainlogo {
    text-decoration: none;
  }
</style>
