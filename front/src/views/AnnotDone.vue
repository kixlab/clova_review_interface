<template>
  <v-container fill-height>
    <v-row justify="center">
    <v-col style="text-align: center;">
      <v-card>
        <v-card-text>
          All the deferred annotations with 'EXACTLY' labels are saved as regular annotations! 
          In the next phase, you will review items that you marked as 'N/A' or 'CAN BE'.
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
export default {
  name: 'AnnotDone',
  data: ()=>{},
  methods: {
    gotoReview: function () {
      var doctype=this.$router.currentRoute.fullPath.split('/')[2];
      this.$router.push('../../review/'+doctype);
    }
  }
}