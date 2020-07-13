<template>
    <v-btn
      class="ma-2"
      :loading="loading"
      :disabled="loading"
      color="secondary"
      @click="loader = 'loading'"
    >
      Submit
    </v-btn>
</template>

<script>
export default {
  name: "ImagePanel",
  data() {
    return {
      loader: null,
      loading: false,
    };
  },
    watch: {
      loader () {
        const l = this.loader
        this[l] = !this[l]

        setTimeout(() => (this[l] = false), 3000)

        this.loader = null
      },
    },
  }
</script>
