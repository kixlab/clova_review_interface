<template>
    <v-col cols="12">
        <v-card>
            <v-card-title style="border-bottom: 0px solid black; background-color: lightgrey;">
                <v-row>
                    <v-col cols="2">
                        <h4>Boxes</h4>
                    </v-col>
                    <v-col cols="8">
                        <h4>Worker Labels</h4>
                    </v-col>
                    <v-col cols="2">
                        <h4>Majority</h4>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-row style="border: 0px solid blue; max-height: 90vh; overflow: scroll; padding: 0; margin-top: 6px;">
                    <v-col cols="2" style="border-right: 1px solid black;">
                        <div v-for="box in image_box" :key="box.id" style="margin: 10px 0;" @mouseover="highlight(box)" @mouseout="undoHighlight(box)">
                            <div v-if="box.hover === true">
                                <span style="border: 2px solid yellow; margin: 0 2px; font-size: 95%; padding: 0 2px;"> <b>{{ box.text }}</b> </span>
                            </div>
                            <div v-else>
                                <span style="border: 2px solid red; margin: 0 2px; font-size: 95%; padding: 0 2px;"> <b>{{ box.text }}</b> </span>
                            </div>
                        </div>
                    </v-col>
                    <v-col cols="8" style="border-right: 1px solid black;">
                        {{image_box.map(v => [v.box_id, v.text])}}
                        {{this.$store.getters.getAnnotatedBoxes}}
                    </v-col>
                    <v-col cols="2">
                    dd
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
//import {mapActions, mapGetters} from 'vuex';
import axios from "axios";
export default {
    name: "IndividualLabel",
    components: {

    },
    data() {
        return {
            image_box : this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id),
        };
    },

    mounted() {
        const self = this;
        this.image_box = this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id);

        this.$store.subscribeAction({after: (action) => {
            if (action.type === 'setImageBoxes' || action.type === 'updateAnnotatedBoxes' || action.type === 'updateImageBoxes') {
                this.image_box = this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id);
            }
        }})

        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-def-annotations/',{
        params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no
        }
        }).then(function(res){
        var annotations=res.data.annotations;
        self.loadAnnotatedBoxes(annotations);})},1000);

    },

    

    methods: {
        highlight(item) { item.hover = true },
        undoHighlight(item) { item.hover = false },
    },

    watch:{
    image_no:{
      deep: true,
      handler(){
        const self=this;
        axios.get(self.$store.state.server_url+'/api/get-def-annotations/',{
          params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no
          }
        }).then(function(res){
          var annotations=res.data.annotations;
          console.log("RECEIVED ANNOTATION ***", res.data.annotations)
          
          setTimeout(
          self.loadAnnotatedBoxes(annotations),1000);

    })
  }}},
}
</script>
<style scoped>

</style>