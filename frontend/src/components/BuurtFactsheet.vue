<template>
  <div v-if="buurten && buurten.length">

    <card title="Algemeen">
      <div class="row">
        <div class="col-lg-6 col-md-12">
          <bag-info-table :buurt="buurt"></bag-info-table>
          <sociale-kenmerken :buurt="buurt"></sociale-kenmerken>
        </div>
        <div class="col-lg-6 col-md-12">
          <amsterdam-map :config="buurtMapConfig" :buurt="buurt"></amsterdam-map>
        </div>
      </div>
      <migratie-achtergrond :buurt="buurt"></migratie-achtergrond>
    </card>

    <card title="Woning bezit">
      <woningen-naar-eigendom :buurt="buurt"></woningen-naar-eigendom>
      <woningen-per-corporatie :buurt="buurt"></woningen-per-corporatie>
      <div class="row">
        <div class="col-lg-6 col-md-12">
        </div>
        <div class="col-lg-6 col-md-12">
          <amsterdam-map :config="afwcMapConfig" :buurt="buurt"></amsterdam-map>
        </div>
      </div>
    </card>

    <card title="Bouwkundige kenmerken">
      <woning-oppervlakten :buurt="buurt"></woning-oppervlakten>
    </card>

    <card title="Bedrijvigheid">
      <div class="row">
        <div class="col-lg-6 col-md-12">
          <gebruiks-overzicht :buurt="buurt"></gebruiks-overzicht>
        </div>
        <div class="col-lg-6 col-md-12">
          <handelsregister-info-table :buurt="buurt"></handelsregister-info-table>
        </div>
      </div>
    </card>

    <card title="Werkzaamheden">
      <gepland-per-corporatie :buurt="buurt"></gepland-per-corporatie>
      <gepland-per-jaar :buurt="buurt"></gepland-per-jaar>
      <div class="row">
        <div class="col-12">
          <amsterdam-mip-table :buurt="buurt"></amsterdam-mip-table>
        </div>
        <div class="col-12">
          <amsterdam-map :config="mipMapConfig" :buurt="buurt"></amsterdam-map>
        </div>
      </div>
    </card>

  </div>
  <div v-else>
    Laden...
  </div>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import card from './Layout/Card'

import AmsterdamMap from './AmsterdamMap'
import afwcMapConfig from '../../static/afwc-map-config'
import mipMapConfig from '../../static/mip-map-config'
import buurtMapConfig from '../../static/buurt-map-config'

import BagInfoTable from './BagInfoTable'
import socialeKenmerken from './SocialeKenmerken'
import migratieAchtergrond from './MigratieAchtergrond'

import HandelsRegisterTable from './HandelsRegisterTable.vue'
import MeerjarigInvesteringsProgrammaTable from './MeerjarigInvesteringsProgrammaTable.vue'
import GeplandPerJaar from './GeplandPerJaar'
import GeplandPerCorporatie from './GeplandPerCorporatie'
import WoningenPerCorporatie from './WoningenPerCorporatie'
import WoningOppervlakten from './WoningOppervlakten'
import WoningenNaarEigendom from './WoningenNaarEigendom'
import GebruiksOverzicht from './GebruiksOverzicht'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt,
      afwcMapConfig,
      mipMapConfig,
      buurtMapConfig
    }
  },
  components: {
    GebruiksOverzicht,
    WoningenNaarEigendom,
    WoningOppervlakten,
    WoningenPerCorporatie,
    GeplandPerCorporatie,
    GeplandPerJaar,
    'card': card,
    'amsterdam-map': AmsterdamMap,
    'bag-info-table': BagInfoTable,
    'sociale-kenmerken': socialeKenmerken,
    'migratie-achtergrond': migratieAchtergrond,
    'handelsregister-info-table': HandelsRegisterTable,
    'amsterdam-mip-table': MeerjarigInvesteringsProgrammaTable
  },
  methods: {
    ...mapActions({
      setBuurt: 'setBuurt'
    })
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  watch: {
    '$route' (to, from) {
      this.buurt = to.params.buurt
    }
  }
}
</script>

<style scoped>
</style>
