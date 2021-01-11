<template>
  <div id="app">
    <histogram />
    <file-list />
    <file-upload />
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue';
import Histogram from './components/Histogram.vue';
import FileList from './components/FileList.vue';

export default {
  name: 'App',
  components: {
    FileUpload,
    Histogram,
    FileList
  },
  mounted() {
    this.$store.dispatch('load')
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
