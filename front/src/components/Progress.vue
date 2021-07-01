<template>
<div class='center'>
  <div style="width: 100%; overflow-x: auto; overflow-y: hidden; position: relative; white-space: nowrap;">
      <template v-for="(status, index) in stats"> 
        <template v-if="index===img_temp">
          <template v-if="status===true">
            <div class="curr done status" v-on:click="goTo(index);" :key='index' style="white-space: normal; display: inline-block; border: 1px solid grey; margin: 1px; white-space: normal;">
            #{{index+1}}
            </div>
          </template>
          <template v-else>
            <div class="curr yet status" v-on:click="goTo(index);" :key='index' style="white-space: normal; display: inline-block; border: 1px solid grey; margin: 1px; white-space: normal;">
            #{{index+1}}
            </div>
          </template>
        </template>
        <template v-else>
          <template v-if="status===true">
            <div class="done status" v-on:click="goTo(index);" :key='index' style="white-space: normal; display: inline-block; border: 1px solid grey; margin: 1px; white-space: normal;">
            #{{index+1}}
            </div>
          </template>
          <template v-else>
            <div class="yet status" v-on:click="goTo(index);" :key='index' style="white-space: normal; display: inline-block; border: 1px solid grey; margin: 1px; white-space: normal;">
            #{{index+1}}
            </div>
          </template>
        </template>
      </template>

  </div>
<!--  <div>
  {{stats}}
 </div>
 --></div>
</template>


<script>
import { mapActions, mapGetters} from 'vuex'

export default {
  name: "Progress",
  data() {
    return {
      image_box: this.$store.getters.getImageBoxes,
      img_temp: this.$store.getters.get_curr_image
    };
  },
  mounted() {
    this.$store.subscribeAction({after: (action) => {
        if (action.type ==='setCurrImage') {
            this.img_temp = this.$store.getters.get_curr_image
            
        }
    }})

  },
  computed: {
    stats() {
      console.log("Hi", this.$store.getters.getStatus);
          return this.$store.getters.getStatus;
        }
  },
  watch: {
    stats() {
      console.log("Hi", this.$store.getters.getStatus);
          return this.$store.getters.getStatus;
        }
  }, 
  methods:{
      ...mapActions(['setCurrImage']),
      ...mapGetters(['getStatus']),
      goTo: function(imgNo){
        this.$store.commit('set_image_count', imgNo);
        this.image_box = this.$store.getters.getImageBoxes;
        this.setCurrImage(imgNo)
      },
  }
};
</script>

<style scoped>
.center{
  margin:auto;
  width: 80% !important;
}
table{
  width: 100% !important;
  overflow-x: scroll;
}
.status{
  margin: auto;
  border: 1px solid grey;
  width: 4%!important;
  cursor:pointer !important;
  
}
.yet{
  background-color: rgba(180, 180, 180, 0.548);
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}

.curr{
  border: 2px solid red !important;
}
</style>
