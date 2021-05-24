<template>
 <v-simple-table>
   <template v-slot:default>
   <tbody>
    <tr>
      <td
        v-for="doc in docs"
        :key="doc.index"
      >#{{doc.index}}
      </td>
    </tr>
   </tbody>
    </template>
 </v-simple-table>
</template>


<script>
import axios from "axios";
//import {mapActions, mapGetters} from 'vuex';

export default {
  name: "Progress",
  data() {
    return {
      image_order: this.$store.state.image_order,
      docs: new Array(20).fill({'status': true}),
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
