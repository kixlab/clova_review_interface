<template>
 <table class='center'>
   <tbody>
    <tr>
      <td v-for="(status, index) in stats" :key='index'
          v-bind:class='{done:(status==true)}'>
          #{{index+1}}
        </td>
    </tr>
   </tbody>
 </table>
</template>


<script>
//import {mapActions, mapGetters} from 'vuex';

export default {
  name: "Progress",
  data() {
    return {
      image_order: this.$store.state.image_order,
    };
  },
  computed: {
    stats () {
        return this.$store.state.annot_status
    }      
}
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
  background-color: rgba(180, 180, 180, 0.548);
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}
</style>
