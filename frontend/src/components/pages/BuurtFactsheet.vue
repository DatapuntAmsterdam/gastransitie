<template>
  <div v-if="buurten && buurtData">

    <card :title="`${buurtData.naam} Algemeen`">
      <div class="row">
        <div class="col-lg-6 col-md-12">
          <buurt-info></buurt-info>
          <sociale-kenmerken></sociale-kenmerken>
        </div>
        <div class="col-lg-6 col-md-12">
          <amsterdam-map :config="buurtMapConfig" :buurt="buurt"></amsterdam-map>
        </div>
      </div>
      <migratie-achtergrond></migratie-achtergrond>
    </card>

    <card :title="`Woning bezit in ${buurtData.naam}`">
      <woningen-naar-eigendom></woningen-naar-eigendom>
      <woningen-per-corporatie></woningen-per-corporatie>
      <div class="row">
        <div class="col-lg-6 col-md-12">
        </div>
        <div class="col-lg-6 col-md-12">
          <amsterdam-map :config="afwcMapConfig" :buurt="buurt"></amsterdam-map>
        </div>
      </div>
    </card>

    <card :title="`Bouwkundige kenmerken ${buurtData.naam}`">
      <woning-oppervlakten></woning-oppervlakten>
    </card>

    <card :title="`Bedrijvigheid in ${buurtData.naam}`">
      <div class="row">
        <div class="col-lg-6 col-md-12">
          <gebruiks-overzicht></gebruiks-overzicht>
        </div>
        <div class="col-lg-6 col-md-12">
          <gevestigde-bedrijven></gevestigde-bedrijven>
        </div>
      </div>
    </card>

    <card :title="`Werkzaamheden in ${buurtData.naam}`">
      <gepland-per-corporatie :buurt="buurt"></gepland-per-corporatie>
      <gepland-per-jaar :buurt="buurt"></gepland-per-jaar>
      <div class="row">
        <div class="col-12">
          <meerjarig-investerings-plan :buurt="buurt"></meerjarig-investerings-plan>
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

import util from '@/services/util'

import card from '../Layout/Card'

import AmsterdamMap from '../AmsterdamMap'
import afwcMapConfig from '../../../static/afwc-map-config'
import mipMapConfig from '../../../static/mip-map-config'
import buurtMapConfig from '../../../static/buurt-map-config'

import socialeKenmerken from '../SocialeKenmerken'
import migratieAchtergrond from '../MigratieAchtergrond'

import GeplandPerJaar from '../GeplandPerJaar'
import GeplandPerCorporatie from '../GeplandPerCorporatie'
import WoningenPerCorporatie from '../WoningenPerCorporatie'
import WoningOppervlakten from '../WoningOppervlakten'
import WoningenNaarEigendom from '../WoningenNaarEigendom'
import GebruiksOverzicht from '../GebruiksOverzicht'
import BuurtInfo from '../BuurtInfo'
import GevestigdeBedrijven from '../GevestigdeBedrijven'
import MeerjarigInvesteringsPlan from '../MeerjarigInvesteringsPlan'

export default {
  data () {
    return {
      afwcMapConfig,
      mipMapConfig,
      buurtMapConfig
    }
  },
  components: {
    MeerjarigInvesteringsPlan,
    GevestigdeBedrijven,
    BuurtInfo,
    GebruiksOverzicht,
    WoningenNaarEigendom,
    WoningOppervlakten,
    WoningenPerCorporatie,
    GeplandPerCorporatie,
    GeplandPerJaar,
    'card': card,
    'amsterdam-map': AmsterdamMap,
    'sociale-kenmerken': socialeKenmerken,
    'migratie-achtergrond': migratieAchtergrond
  },
  methods: {
    ...mapActions({
      setBuurt: 'setBuurt',
      setBuurtData: 'setBuurtData'
    }),
    async loadBuurt (buurt) {
      this.setBuurt(buurt)
      if (this.buurten) {
        const buurtDetail = this.buurten.find(b => b.vollcode === buurt)
        const url = 'https://api.data.amsterdam.nl/gebieden/buurt/' + buurtDetail.landelijk
        const buurtData = await util.readData(url)
        this.setBuurtData(buurtData)
      } else {
        this.setBuurtData(null)
      }
    }
  },
  computed: {
    ...mapGetters([
      'buurten',
      'buurt',
      'buurtData'
    ])
  },
  watch: {
    '$route' (to) {
      this.loadBuurt(to.params.buurt)
    },
    'buurten' () {
      this.loadBuurt(this.buurt)
    }
  },
  mounted () {
    this.loadBuurt(this.$route.params.buurt)
  }
}
</script>

<style scoped>
</style>
