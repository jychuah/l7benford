<template>
  <div>
    <h1>Benford Distribution</h1>
    <div v-if="isLoading">
      <h3>
        Loading...
      </h3>
    </div>
    <div v-else>
      <h3>{{ filename }}</h3>
      <div>
        <label>Select a field</label>
        <select :value="selectedField" @change="selectField($event)">
          <option v-for="field in fields" :key="field">{{ field }}</option>
        </select>
      </div>
      <div>
        <label>Don't see the correct fields? Change the file delimiter</label>
        <select :value="delimiter" @change="reparse({ $event, filename })">
          <option value="tab">Tabs</option>
          <option value="comma">Commas</option>
        </select>
      </div>
      <vue-plotly :data="data" :layout="layout" />

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
        delimiter: state => state.selected ? state.selected.delimiter : '',
        filename: state => state.selected ? state.selected.filename : '',
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
        selectedField: state => state.selected ? state.selected.field : null,
        fields: state => state.selected ? Object.keys(state.selected.histogram): [],
        isLoading: state => state.loading
      })
    },
    methods: {
      ...mapActions([
        'selectField',
        'reparse'
      ])
    },
    components: {
      VuePlotly,
    }
  }
</script>

<style>
  select {
    margin-left: 1em;
  }
</style>