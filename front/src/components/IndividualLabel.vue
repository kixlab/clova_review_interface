<template>
    <v-col cols="12">
        <v-card>
            <v-card-title style="border-bottom: 0px solid black; background-color: lightgrey;">
                <v-row>
                    <v-col cols="2">
                        <h4>Boxes</h4>
                    </v-col>
                    <v-col cols="3">
                        <h4>Worker 1</h4>
                    </v-col>
                    <v-col cols="3">
                        <h4>Worker 2</h4>
                    </v-col>
                    <v-col cols="3">
                        <h4>Worker 3</h4>
                    </v-col>
                    <v-col cols="1">
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
                    <v-col cols="3" v-for="(userannot, index) in worker_annots" :key="index" style="border-right: 1px solid black;">
                        <!--{{image_box.map(v => [v.box_id, v.text])}}-->
                        <div v-for="box in userannot.annotations" :key="'annot-'+userannot.user+box.box_id">
                            <v-btn text small tile depressed v-bind:class="{success: box.confidence, error: (box.subcat=='N/A'), warning: !box.confidence}"> 
                                    {{box.cat}}-{{box.subcat}} 
                            </v-btn>
                        </div>
                        <!--{{this.$store.getters.getAnnotatedBoxes}}-->
                    </v-col>
                    <v-col cols="1">
                    dd
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
import axios from "axios";
import {mapActions, mapGetters} from 'vuex';

export default {
    name: "IndividualLabel",
    components: {

    },
    data() {
        return {
            image_box : this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id),
            annotated_box: this.$store.getters.getAnnotatedBoxes,
            worker_annots: []
        };
    },

    mounted() {
        const self = this;
        this.image_box = this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id);
        this.annotated_box = this.$store.getters.getAnnotatedBoxes;

        this.$store.subscribeAction({after: (action) => {
            if (action.type === 'setImageBoxes' || action.type === 'updateAnnotatedBoxes' || action.type === 'updateImageBoxes') {
                this.image_box = this.$store.getters.getImageBoxes.sort((a, b) => a.box_id - b.box_id);
            }
            if (action.type === 'updateAnnotatedBoxes' || action.type === 'loadAnnotatedBoxes' || action.type === 'setCurrImage' || action.type === 'updateImageBoxes') {
                this.annotated_box = this.$store.getters.getAnnotatedBoxes;
            }
        }})

        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-worker-annotations/',{
        params:{
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no
        }
        }).then(function(res){
           self.worker_annots=res.data.workerannots;
        console.log(res.data.workerannots);
//            self.loadAnnotatedBoxes(annotations);
        })},1000);

    },

    
    methods: {
        ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes', 'setCurrImage']),
        ...mapGetters(['getImageBoxes']),

        highlight(item) { item.hover = true },
        undoHighlight(item) { item.hover = false },

        highlightGroup(group) {
            for (var box in group) {
                group[box].hover = true;
            }
        },

        undoHighlightGroup(group) {
            for (var box in group) {
                group[box].hover = false;
            }
        },

        loadAnnotatedBoxes(annotations){
            const self = this;
            self.updateAnnotatedBoxes([[], "reset"])
            var currImageBox = self.$store.getters.getImageBoxes
            for (var gno in annotations){
            var agroup=annotations[gno]
            var group=[]
            var ids=agroup.boxes_id.replace("[","").replace("]","").replace(" ","").replace(', ',',').split(',')
            for(var id in ids){
                var box_id=parseInt(ids[id])
                var currBox=currImageBox[box_id]
                if((currBox==undefined)||(currBox.box_id!=box_id)){
                currBox=currImageBox[box_id-1];
                }
                currBox.annotated=true
                group.push(currBox)
            }
            //console.log(currImageBox)
            self.updateImageBoxes(currImageBox)
            self.updateAnnotatedBoxes([{cat: agroup.cat, subcat: agroup.subcat, subcatpk: agroup.subcatpk, catpk: agroup.catpk, boxes: group, confidence: agroup.confidence, annotpk: agroup.group_id}, "add"])
            }          
        },
      clicked(label) {
        console.log("Clicked", label)
      }
    },

    computed: {
        ...mapGetters(['image_no'])
    },

    watch: {
        image_no: {
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
                    setTimeout(self.loadAnnotatedBoxes(annotations),1000);
                })
            }
        }
    },
}
</script>

<style scoped>

.error.warning{
  background-color: #ff5252 !important;
  color: white !important;

}
</style>

