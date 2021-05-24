<template>
 <v-table>
   <tbody>
    <tr>
      <td
        v-for="doc in documents1"
        :key="doc.no"
      >#{{doc.no}}
      </td>
    </tr>
    <tr>
      <td
        v-for="doc in documents2"
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
      documents1: new Array(10).fill(0),
      documents2: new Array(10).fill(0)
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
