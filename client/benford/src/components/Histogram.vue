<template>
  <div>
    <h1>Benford</h1>
    <div v-if="isLoading">
      <h3>
        Loading...
      </h3>
    </div>
    <div v-else>
      <h3>{{ filename }}</h3>
      <vue-plotly :data="data" :layout="layout" />
      <div>
        <select v-model="delimiter" @change="reparse(filename, delimiter)">
          <option disabled value="">Please select one</option>
          <option value="tab">Tab</option>
          <option value="comma">Comma</option>
        </select>
      </div>
    </div>
</div>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import VuePlotly from '@statnett/vue-plotly'

  const digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]

  export default {
    name: 'histogram',
    computed: {
      layout: function() {
        return {
          xaxis: {
            dtick: 1
          }
        }
      },
      ...mapState({
        delimiter: state => state.selected ? state.selected.delimiter : null,
        filename: state => state.selected.filename,
        data: state => state.selected && state.files[state.selected.filename]
          ? [
              {
                x: digits,
                y: [.301, .176, .125, .097, .079, .067, .058, .051, .046],
                type: 'bar',
                name: 'Benford Distrubtion'
              },
              {
                x: digits,
                y: Object.values(state.files[state.selected.filename].histogram[state.selected.field]),
                type: 'bar',
                name: state.selected.field
              }
            ]
          : [],
        isLoading: state => state.loading
      })
    },
    methods: {
      ...mapActions([
        'reparse'
      ])
    },
    components: {
      VuePlotly
    }
  }
</script>

<style lang="scss">
</style>