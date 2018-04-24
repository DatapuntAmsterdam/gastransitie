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
                <legend-bullet :color="COLORS[index]"></legend-bullet>
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
      <div class="col-lg-6 col-md-6 piecontainer">
        <div class="piechart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import _ from 'lodash'
import LegendBullet from './LegendBullet'
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
  components: {LegendBullet},
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
      data: [],
      COLORS
    }
  },
  methods: {
    prepData (buurtData) {
      // We want a piechart that is sorted piechart containing the top five large
      // owners of "verblijfsobjecten" and the sum of all small owners. Goal is to
      // be able to quickly judge the how fragmented the ownership in a neighborhood
      // is (few large owners mean easier time coordinating / negotiating).
      // Any owner without a "statutaire naam" is dropped (we want corporation here -
      // and not show persons).
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

      // Show small owners as one category at the end.
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
      // Typical D3 piechart, we are not, however, using the update selection mechanism to
      // update data in case of new data, we just redraw.

      // Find element to append plot to, set correct size etc.
      let root = d3.select(this.$el).select('.piechart')
      root.selectAll().remove()

      let svg = root.append('svg')
        .attr('width', WIDTH)
        .attr('height', HEIGHT)

      let g = svg.append('g')
        .attr('transform', 'translate(' + WIDTH / 2 + ',' + HEIGHT / 2 + ')')

      // "pie generator" (d3.pie) generates data that can be handed to a the SVG arc
      // generator (d3.arc) which provide the content for the "d" property of SVG path
      // elements that are added to the DOM.
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
  .piecontainer {
    text-align: center;
    margin: auto;
  }
</style>
