<template>
  <div>
    <form enctype="multipart/form-data" novalidate>
      <h3>Upload</h3>
      <div class="dropbox">
        <input type="file" :disabled="isUploading" @change="upload($event.target.files[0]);" class="input-file">
          <p v-if="isUploading">
            Uploading files...
          </p>
          <p v-else>
            Click to browse
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