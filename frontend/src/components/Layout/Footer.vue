<template>
  <div class="row bg-darkgrey footer">
    <footer class="container footer-component">
      <div class="row">
        <div class="col-12">
          <h2>Disclaimer</h2>
          <p>
            Dashboard {{title}} is gemaakt door {{author}}.
          </p>
          <p>
            De inhoud van dashboard {{title}} is met uiterste zorgvuldigheid tot stand gebracht.
            De inhoud wordt regelmatig gecontroleerd en geactualiseerd.
          </p>
          <p>
            {{author}} kan echter niet aansprakelijk worden gesteld voor de juistheid, volledigheid en actualiteit van de website.
            {{author}} kan in het bijzonder niet aansprakelijk worden gesteld voor eventuele schade of consequenties ontstaan door direct of indirect gebruik van de inhoud van de website.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>

export default {
  name: 'AMSFooter',
  props: [
    'title'
  ],
  components: {
  },
  data () {
    return {
      author: 'Datapunt Amsterdam'
    }
  },
  computed: {
  },
  methods: {
  },
  watch: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
