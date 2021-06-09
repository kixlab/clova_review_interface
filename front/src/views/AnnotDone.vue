<template>
  <v-container fill-height>
    <v-row justify="center">
    <v-col style="text-align: center;">
      <v-card>
        <v-card-text>
          <p>In the next phase, you will review items that you marked as 'N/A' or 'CAN BE'.</p>
          <p>All the deferred annotations with 'EXACTLY' labels are saved as regular annotations!</p> 
        </v-card-text>
         <v-btn
            @click="gotoReview()"
            color="deep-purple accent-2"
            class="mr-4"
            style="margin-left: auto;"
            large
          >
            Next
          </v-btn>
      </v-card>
      <br>
    </v-col>
    </v-row>
  </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: 'AnnotDone',
  methods: {
    gotoReview: function () {
      var doctype=this.$router.currentRoute.fullPath.split('/')[2];
      var self=this;
      
      axios.post(self.$store.state.server_url + "/api/save-as-regular/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
          }).then(function () {
            self.$router.push('../../review/'+doctype);
          });

    },
  }
}
</script>