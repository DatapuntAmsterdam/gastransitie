<template>
    <div>
      <transition name="fade">
        <div class="page-overlay" v-if="!simple && showSpinner">
          <div class="progress-wrapper">
            <div class="loader"></div>
            <div class="progress-txt">Laden...</div>
          </div>
        </div>
        <div class="progress-indicator progress-red" v-if="simple"></div>
      </transition>
    </div>
</template>

<script>
import { HTTPStatus } from '@/services/datareader'

export default {
  name: 'LoadingComponent',
  components: {
  },
  props: {
    simple: {
      default: false,
      type: Boolean
    }
  },
  data () {
    return {
      HTTPStatus,
      showSpinner: false
    }
  },
  methods: {
    shouldShowSpinner (pending) {
      if (pending > 0) {
        clearTimeout(this.spinnerHideTimeout)
        this.showSpinner = true
      } else {
        this.spinnerHideTimeout = setTimeout(() => {
          this.showSpinner = false
        }, 300)
      }
    }
  },
  watch: {
    'HTTPStatus.pending': function (pending) {
      this.shouldShowSpinner(pending)
    }
  }
}
</script>

<style lang="scss" scoped>
 @import "~stijl/scss/ams-colorpalette";

 $progress-background: $ams-middengrijs;

 .progress-wrapper {
   background: $progress-background !important;
   border-color: $ams-donkergrijs;
 }

 .progress-indicator::before {
   background-color: $progress-background !important;
 }

 .progress-indicator::after {
   background-color: $progress-background !important;
 }

 .page-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 8888;
}

.page-overlay .progress-wrapper {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  margin: 1rem;
  background-color: #fff;
  z-index: 99999;
  text-align: center;
}

.loader {
  border: 10px solid $progress-background;
  border-top: 10px solid $ams-rood;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active {
  transition: opacity .2s ease-out;
}

.fade-leave-active {
  transition: opacity .3s ease-in;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
