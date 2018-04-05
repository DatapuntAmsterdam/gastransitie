<template>
  <div>
    <div class="row">
      <div class="col-lg-6 col-md-6">
        <table class="table table-hover table-responsive" v-if="data.length">
          <thead>
            <tr>
              <th></th>
              <th>Eigenaar</th>
              <th>Aantal woningen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in data" :key="item.naam">
              <td>
                <span :style="getBulletStyle(index)" class="legend-bullet">&#9634;</span>
              </td>
              <td>
                {{item.naam}}
              </td>
              <td>
                {{item.aantal}}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="col-lg-6 col-md-6 piechart"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import _ from 'lodash'
// edit for layout tweaks:
const HEIGHT = 300 // Height of SVG element containing pie chart
const FONT_SIZE = 12 // Font size used in pie chart
const N_LARGE_OWNERS = 5 // Number of large "verblijfs object" (~ dwelling) owners

// layout constants
const WIDTH = HEIGHT
const OUTER_RADIUS = HEIGHT / 2
const INNER_RADIUS = HEIGHT / 4
const TEXT_RADIUS = (OUTER_RADIUS + INNER_RADIUS) / 2

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
      data: []
    }
  },
  methods: {
    prepData (buurtData) {
      let statutairEigenaar = _.slice(
        _.filter(
          _.sortBy(buurtData.data.groot_bezitters, item => -item.thecounts),
          item => item.statutaire_naam
        ).map(
          item => ({naam: item.statutaire_naam, aantal: item.thecounts})
        ),
        0,
        N_LARGE_OWNERS
      )

      return _.sortBy(statutairEigenaar, item => -item.aantal).concat(
        [{naam: 'Eigenaar / Bewoner', aantal: buurtData.data.bewoners_count}]
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
        .outerRadius(OUTER_RADIUS)
        .innerRadius(INNER_RADIUS)

      let label = d3.arc()
        .outerRadius(TEXT_RADIUS)
        .innerRadius(TEXT_RADIUS)

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
        .style('vertical-align', 'middle')
        .style('font-size', FONT_SIZE)
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
