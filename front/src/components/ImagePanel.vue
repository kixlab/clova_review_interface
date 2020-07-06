<template>
  <v-card
    tile
    width="100%"
    height="100%"
    >
    I am ImagePanel!
    <v-img :src=image_url contain width="400px" height="500px" />
    <v-btn @click="loadImage">Load an image from the server</v-btn>

  </v-card>
</template>


<script>
import axios from "axios";
export default {
  name: "ImagePanel",
  data() {
    return {
      image_url: '../assets/logo.png'
    };
  },
  methods: {
    loadImage: function() {
      const self = this;
      axios.get("http://localhost:8000/api/image/")
        .then(function (res) {
        // console.log(res.data)
        self.image_url = "http://localhost:8000" + res.data
      })
      .catch(function(err) {
        alert(err);
      });
    }
  }
};
</script>