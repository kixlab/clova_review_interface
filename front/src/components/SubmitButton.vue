<template>
    <v-btn
      class="ma-2"
      :loading="loading"
      :disabled="loading"
      color="secondary"
      @click="onSubmit"
    >
      Submit
    </v-btn>
</template>

<script>
import axios from "axios";

export default {
  name: "ImagePanel",
  data() {
    return {
      loading: false,
    };
  },
  methods: {
    onSubmit: function() {
      const that = this;
      that.loading = true

      axios.post("http://localhost:8000/api/image/", {
        test: 'testText'
      })
      .then(function (res) {
        console.log(res)
        that.loading = false
        alert("Server responded!!")
      })

      .catch(function(err) {
        that.loading = false
        alert(err);
      });

    }
  }
  }
</script>
