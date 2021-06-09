<template>
  <v-tooltip bottom :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :disabled="disabled"
        color="error"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Submit
      </v-btn>
      </div>
    </template>
    Annotate all the images to submit!
  </v-tooltip>
</template>

<script>
//import axios from "axios";
//import {mapActions} from 'vuex';

export default {
  name: "SubmitButton",
  methods: {
    onSubmit: function() {
      var doctype=this.$router.currentRoute;
      console.log(doctype);
     // this.$router.push('../annot-done')
 }
  },

  computed: {
    disabled() {
      return false

//      return !this.$store.getters.getIfAllImagesAnnotated
    }
  }
}
</script>
