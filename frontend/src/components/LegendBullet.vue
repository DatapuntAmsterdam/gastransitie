<template>
  <span :style="getBulletStyle(color)" class="legend-bullet">
    &#9724;
  </span>
</template>

<script>
export default {
  name: 'legend-bullet',
  props: [
    'color'
  ],
  methods: {
    getBulletStyle (color) {
      return {
        'background': color,
        color
      }
    }
  }
}
</script>

<style scoped>
.legend-bullet {
  letter-spacing: 2px;
  border: 1px solid;
  margin-right: 7px;
  fill-opacity: 1;
  fill: blue;
  -webkit-print-color-adjust: exact !important;   /* Chrome, Safari */
  color-adjust: exact !important;                 /*Firefox*/
}
</style>
