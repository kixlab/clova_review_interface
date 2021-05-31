<template>
 <table class='center'>
   <tbody>
    <tr>
      <td v-for="(status, index) in stats" :key='index'
          v-bind:class='{done:(status==true), yet:(status==false)}'>
          #{{index+1}}
        </td>
    </tr>
   </tbody>
 </table>
</template>


<script>
//import {mapGetters } from 'vuex'

export default {
  name: "Progress",
  data() {
    return {
      image_order: this.$store.state.image_order,
      stats: this.$store.state.annot_status
    };
  },
  mounted() {
    this.$store.subscribeAction((action) => {
        if (action.type === 'setStatus' || action.type==='setAStatus') {
            this.stats = this.$store.state.annot_status
            console.log('stats updated')
            console.log(this.stats)
            
        }
    })

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
}
.yet{
  background-color: rgba(180, 180, 180, 0.548);
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}
</style>
