<template>
 <table class='center'>
   <tbody>
    <tr>
      <td v-for="(status, index) in stats" :key='index'
          v-bind:class='status? done:yet'>
          #{{index+1}}
        </td>
    </tr>
   </tbody>
 </table>
</template>


<script>
import axios from "axios";
//import {mapActions, mapGetters} from 'vuex';

export default {
  name: "Progress",
  data() {
    return {
      image_order: this.$store.state.image_order,
      stats: new Array(20).fill({'status': true}),
    };
  },

  mounted: function() {
    const self = this;
    axios.get(self.$store.state.server_url + "/api/get-status",{
    params:{
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType
      }
    }).then(function(res){
      console.log(res)
      })
  },
};
</script>

<style scoped>
.center{
  margin:auto;
  min-width: 80% !important;
}
td{
  margin: auto;
  border: 1px solid grey;
}
.done{
  background-color: rgba(79, 192, 79, 0.548);
}

.yet{
  background-color: rgba(192, 79, 79, 0.548);
}
</style>
