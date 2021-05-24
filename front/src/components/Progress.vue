<template>
 <v-table>
   <tbody>
    <tr>
      <td
        v-for="doc in docs"
        :key="doc.no"
      >#{{doc.no}}
      </td>
    </tr>
   </tbody>
 </v-table>
</template>


<script>
import axios from "axios";
//import {mapActions, mapGetters} from 'vuex';

export default {
  name: "Progress",
  data() {
    return {
      image_order: this.$store.state.image_order,
      docs: new Array(20).fill({'no': 1, 'status': true}),
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
