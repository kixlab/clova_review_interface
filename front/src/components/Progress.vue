<template>
<div class='center'>
 <table >
   <tbody>
    <tr>
      <template v-for="(status, index) in stats" > 
        <template v-if="status === true">
          <td class="done" v-on:click="goTo(index);" :key='index'>
          #{{index+1}}
          </td>
        </template>
        <template v-else-if="status === false">
          <td class="yet" v-on:click="goTo(index);" :key='index'>
          #{{index+1}}
          </td>
        </template>
        
      </template>
      
    </tr>
   </tbody>
 </table>
<!--  <div>
  {{stats}}
 </div>
 --></div>
</template>


<script>
//import { mapActions, mapGetters } from 'vuex'

export default {
  name: "Progress",
  data() {
    return {
      stats: this.$store.getters.status,
      image_box: this.$store.getters.getImageBoxes
    };
  },
  mounted() {
    this.$store.subscribeAction({after: (action) => {
        if (action.type ==='setAStatus' || action.type === 'setImageBoxes') {
            this.stats = this.$store.getters.status;
            console.log('stats updated')
            console.log("***", this.stats)
            
        }
    }})

  },
  methods:{
      goTo: function(imgNo){
        this.$store.commit('set_image_count', imgNo);
        this.image_box = this.$store.getters.getImageBoxes;
      },
  }
};
</script>

<style scoped>
.center{
  margin:auto;
  min-width: 80% !important;
}
table{
  width: 100% !important;
}
td{
  margin: auto;
  border: 1px solid grey;
  width: 5%!important;
  cursor:pointer !important;
}
.yet{
  background-color: rgba(180, 180, 180, 0.548);
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}
</style>
