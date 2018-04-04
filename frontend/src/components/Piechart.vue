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

const N_LARGE_OWNERS = 10
const COLORS = d3.schemePaired.slice(0, N_LARGE_OWNERS)
COLORS.push('gray')

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
      let statutairEigenaar = _.slice(
        _.filter(
          _.sortBy(buurtData.data.groot_bezitters, item => -item.aantal),
          item => item.statutaire_naam
        ).map(
          item => ({naam: item.statutaire_naam, aantal: item.thecounts})
        ),
        0,
        N_LARGE_OWNERS
      )

      let overige = buurtData.data.vbo_count - statutairEigenaar.reduce((sum, item) => sum + item.aantal, 0)
      return _.sortBy(statutairEigenaar, item => -item.aantal).concat(
        [{naam: 'Overige', aantal: overige}]
      )
    },
    getBulletStyle (index) {
      const color = COLORS[index]
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
        .outerRadius(HEIGHT / 2)
        .innerRadius(HEIGHT / 4)

      let label = d3.arc()
        .outerRadius(HEIGHT / 2 - 50)
        .innerRadius(HEIGHT / 2 - 50)

      let arc = g.selectAll('.arc')
        .data(pie(data))
        .enter().append('g')
        .attr('class', 'arc')

      arc.append('path')
        .attr('d', path)
        .attr('fill', (d, i) => COLORS[i])

      arc.append('text')
        .attr('transform', d => 'translate(' + label.centroid(d) + ')')
        .text(function (d) {
          return (180 * (d.endAngle - d.startAngle) / Math.PI) > 20 ? d.data.aantal : ''
        })
        .style('text-anchor', 'middle')
    },
    draw (buurtData) {
      if (buurtData) {
        this.data = this.prepData(buurtData)
        this.drawPieChart(this.data)
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
