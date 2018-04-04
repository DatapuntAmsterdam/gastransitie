<template>
  <div>
      <div class="row">
        <div class="col-lg-6 col-md-12 piechart">
        </div>
        <div class="col-lg-6 col-md-12 pielegend">
          <table>
            <thead>
              <tr>
                <th>Kleur</th>
                <th>Aantal</th>
                <th>Eigenaar</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="data.length" v-for="(item, index) in data" :key="item.naam">
                <td class="legend-entry">
                  <span :style="getBulletStyle(index)" class="legend-bullet">
                    &#9634;
                  </span>
                </td>
                <td>{{item.aantal}}</td>
                <td>{{item.naam}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import _ from 'lodash'

const WIDTH = 400
const HEIGHT = 400

export default {
  props: [
    'buurtData'
  ],
  watch: {
    buurtData (to) {
      this.draw(to)
    }
  },
  data () {
    return {
      data: null
    }
  },
  methods: {
    prepData (buurtData) {
      // Owners with more than 5 dwellings, and no "statutaire_naam".
      let overige = _.filter(this.buurtData.data.groot_bezitters, item => !(item.statutaire_naam))
      let overigeSum = overige.reduce((sum, item) => sum + item.thecounts, 0)
      let overigeEigenaar = [{naam: 'Overige', aantal: overigeSum}]

      // Owners with more than 5 dwellings and a "statutaire_naam"
      let statutairEigenaar = (_.filter(buurtData.data.groot_bezitters, item => item.statutaire_naam)).map(
        item => ({naam: item.statutaire_naam, aantal: item.thecounts})
      )

      // owner-occupiers
      let bewonerEigenaar = [{naam: 'Eigenaar en bewoner', aantal: buurtData.data.bewoners_count}]

      return [].concat(statutairEigenaar, overigeEigenaar, bewonerEigenaar).sort()
    },
    getBulletStyle (index) {
      const color = d3.schemePaired[index % d3.schemePaired.length]
      return {
        'background-color': color,
        color: color
      }
    },
    drawPieChart (data) {
      let root = d3.select(this.$el).select('.piechart')
      root.selectAll().remove()

      let svg = root.append('svg')
        .attr('width', WIDTH)
        .attr('height', HEIGHT)

      let g = svg.append('g')
        .attr('transform', 'translate(' + WIDTH / 2 + ',' + HEIGHT / 2 + ')')

      let pie = d3.pie()
        .value(d => d.aantal)
        .sort(null)

      let path = d3.arc()
        .outerRadius(HEIGHT / 2 - 20)
        .innerRadius(HEIGHT / 4)

      let arc = g.selectAll('.arc')
        .data(pie(data))
        .enter().append('g')
        .attr('class', 'arc')

      arc.append('path')
        .attr('d', path)
        .attr('fill', (d, i) => d3.schemePaired[i % d3.schemePaired.length])
    },
    draw (buurtData) {
      if (buurtData) {
        this.data = this.prepData(buurtData)
        this.drawPieChart(this.data)

        // Eigenaar bewoners: data.bewoners_count
        // overig: data.groot_bezitters
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.legend-entry {
  margin-top: .3rem;
}

.legend-bullet {
  letter-spacing: 2px;
  border: 1px solid;
  margin-right: 7px;
}
</style>
