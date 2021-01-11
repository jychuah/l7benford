<template>
  <div>
    <form enctype="multipart/form-data" novalidate>
      <h1>Upload</h1>
      <div class="dropbox">
        <input type="file" :disabled="isUploading" @change="upload($event.target.files[0]);" class="input-file">
          <p v-if="isUploading">
            Uploading {{ fileCount }} files...
          </p>
          <p v-else>
            Drag your file(s) here to begin<br> or click to browse
          </p>
      </div>
    </form>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex';

  export default {
    name: 'file-upload',
    computed: mapState({
      isUploading: state => state.upload.status === 'UPLOADING',
      error: state => state.upload.error,
    }),
    methods: {
      ...mapActions([
        'upload'
      ])
    }
  }
</script>

<style lang="scss">
</style>