<template>
<div class='center' style="border: 1px solid black; background-color: white;">
  <h2 style="margin-bottom: 5px;">Images </h2>
  <div style="height: 80vh; overflow-x: hidden; overflow-y: scroll; position: relative; white-space: nowrap;">
      <div v-for="(status, index) in stats" :key="index"> 
        <template v-if="index===img_temp">
          <template v-if="status===true">
            <button class="curr done status" v-on:click="goTo(index);" :key='index' >
            <b>#{{index+1}}</b>
            </button>
          </template>
          <template v-else>
            <button class="curr yet status" v-on:click="goTo(index);" :key='index'>
            <b>#{{index+1}}</b>
            </button>
          </template>
        </template>
        <template v-else>
          <template v-if="status===true">
            <button class="done status" v-on:click="goTo(index);" :key='index' >
            <b>#{{index+1}}</b>
            </button>
          </template>
          <template v-else>
            <button class="yet status" v-on:click="goTo(index);" :key='index' >
            <b>#{{index+1}}</b>
            </button>
          </template>
        </template>
      </div>

  </div>
  <!--
  <div style="height: 100%; overflow-x: auto; overflow-y: hidden; position: relative; white-space: nowrap;">
      <template v-for="(status, index) in stats"> 
        <template v-if="index===img_temp">
          <template v-if="status===true">
            <button class="curr done status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
          <template v-else>
            <button class="curr yet status" v-on:click="goTo(index);" :key='index'>
            #{{index+1}}
            </button>
          </template>
        </template>
        <template v-else>
          <template v-if="status===true">
            <button class="done status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
          <template v-else>
            <button class="yet status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
        </template>
      </template>

  </div>
  -->
</div>
</template>


<script>
import { mapActions, mapGetters} from 'vuex'

export default {
  name: "Progress",
  data() {
    return {
      image_box: this.$store.getters.getImageBoxes,
      img_temp: this.$store.getters.get_curr_image,
      stats: new Array(1000).fill(false)
    };
  },
  mounted() {
    this.$store.subscribeAction({after: (action) => {
        if (action.type ==='setCurrImage') {
            this.img_temp = this.$store.getters.get_curr_image
            
        }
    }})

  },
 /*  computed: {
    stats() {
          return 
        }
  }, */
  /* watch: {
    stats() {
      console.log("Hi", this.$store.getters.getStatus);
          return this.$store.getters.getStatus;
        }
  }, */ 
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
  width: 90% !important;
}
table{
  width: 100% !important;
  overflow-x: scroll;
}
.status{
  margin: 2px;
  border: 0px solid grey;
  border-radius: 2% !important;
  padding: 3px;
  cursor:pointer !important;
  height: 30px; 
  width: 90%;
}
.yet{
  background-color: #A6C3EB;
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}

.curr{
  border: 3px solid red !important;
}
</style>
