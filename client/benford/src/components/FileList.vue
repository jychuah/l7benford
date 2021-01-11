<template>
  <div>
    <h3>Files</h3>
    <div v-for="file in files" :key="file">
      <a 
        v-if="filename !== file"
        href="#" @click="selectFile({ $event, file })"
      >
        {{ file }}
      </a>
      <b v-else>{{ file }}</b>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex';

  export default {
    name: 'file-list',
    computed: {
      ...mapState({
        files: state => Object.keys(state.files),
        filename: state => state.selected ? state.selected.filename : ''
      })
    },
    methods: {
      ...mapActions([
        'selectFile'
      ])
    }
  }
</script>

<style>
</style>