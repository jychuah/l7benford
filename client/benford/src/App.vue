<template>
  <div id="app">
    <file-upload />
    <histogram />
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue';
import Histogram from './components/Histogram.vue';

export default {
  name: 'App',
  components: {
    FileUpload,
    Histogram
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
