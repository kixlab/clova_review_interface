<template>
    <v-col cols="12">
        <v-card>
            <v-card-title style="border-bottom: 0px solid black; background-color: lightgrey;">
                <v-row>
                    <v-col cols="2">
                        <h4>Boxes (Total-{{this.$store.getters.getImageBoxes.length}})</h4>
                    </v-col>
                    <v-col v-for="(userannot, index) in worker_annots" :key="index">
                        <h4>Worker {{index+1}} - {{worker_annots[index].user}}</h4>
                    </v-col>
                    <v-col cols="2">
                        <h4>Majority</h4>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-row style="border: 0px solid blue; max-height: 90vh; overflow: scroll; padding: 0; margin-top: 6px;">
                    <v-col cols="2" style="border-right: 1px solid black;padding: 0px;">
                        <div v-for="box in image_box" :key="box.id" class="datarow"  @mouseover="highlight(box)" @mouseout="undoHighlight(box)">
                            <div v-if="box.hover === true">
                                <span style="border: 2px solid yellow; margin: 0 2px; font-size: 95%; padding: 0 2px;"> <b>{{ box.text }}</b> </span>
                            </div>
                            <div v-else>
                                <span style="border: 2px solid red; margin: 0 2px; font-size: 95%; padding: 0 2px;"> <b>{{ box.text }}</b> </span>
                            </div>
                        </div>
                    </v-col>
                    <v-col v-for="(userannot, index) in worker_annots" :key="index" style="border-right: 1px solid black; padding: 0px;">
                        <!--{{image_box.map(v => [v.box_id, v.text])}}-->
                        <div v-for="box in userannot.annotations" :key="'annot-'+userannot.user+box.box_id" class="datarow">
                            <v-btn text small v-bind:class="{exactly: box.confidence, na: (box.subcat=='N/A'), canbe: !box.confidence}"> 
                                    {{box.cat}}-{{box.subcat}} 
                            </v-btn>
                        </div>
                        
                    </v-col>
                    <v-col cols="2" style="padding: 0px;">
                        <div v-for="box in majority_list" :key="'annot-'+box.box_id" class="datarow">
                            <div v-if="box.confidence && box.catMajority===3 && box.subcatMajority===3">
                                <v-btn text small style="color: green"> 
                                    {{box.cat}}-{{box.subcat}}
                                </v-btn>

                            </div>
                            <div v-else>
                                <v-btn text small style="color: black"> 
                                    {{box.cat}}-{{box.subcat}}
                                </v-btn>
                            </div>
                        </div>
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
            worker_annots: [{'user': null, 'annotations': []},{'user': null, 'annotations': []},{'user': null, 'annotations': []}],
            headers:[
                {
                text: 'Boxes',
                align: 'start',
                sortable: false, 
                value: ''
                }
            ],
            majority_list: [],
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
            /*
            for (var i in res.data.workerannots) {
                console.log("&&&&&", res.data.workerannots[i].user + " -- " + res.data.workerannots[i].annotations.length)
            }*/
            var majority = []
            for (var i in res.data.workerannots[0].annotations) {
                majority.push(self.majority_three(res.data.workerannots[0].annotations[i], res.data.workerannots[1].annotations[i], res.data.workerannots[2].annotations[i]))
            }
            self.majority_list = majority
            console.log("MAJORITY - ", majority)
        })},1000);

    },

    
    methods: {
        ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes', 'setCurrImage']),
        ...mapGetters(['getImageBoxes']),

        highlight(item) { item.hover = true },
        undoHighlight(item) { item.hover = false },

        /* highlightGroup(group) {
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
        }, */
      /* clicked(label) {
        console.log("Clicked", label)
      } */

        majority_three(label1, label2, label3) {
            var conf = true
            var box_id = label1.box_id
            if (label1.confidence && label2.confidence && label3.confidence) {
                conf = true
            }
            else {
                conf = false
            }
            if (label1.cat === label2.cat && label2.cat === label3.cat) {
                if (label1.subcat === label2.subcat && label1.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 3, subcatMajority: 3}
                }
                else if (label1.subcat === label2.subcat || label1.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 3, subcatMajority: 2}
                }
                else if (label2.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label2.subcat, confidence: conf, box_id: box_id, catMajority: 3, subcatMajority: 2} 
                }
                else {
                    return {cat: label1.cat, subcat: "N/A", confidence: conf, box_id: box_id, catMajority: 3, subcatMajority: 1} 
                }
            }
            else if (label1.cat === label2.cat || label1.cat === label3.cat) {
                if (label1.subcat === label2.subcat && label1.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 3}
                }
                else if (label1.subcat === label2.subcat || label1.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 2}
                }
                else if (label2.subcat === label3.subcat) {
                    return {cat: label1.cat, subcat: label2.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 2} 
                }
                else {
                    return {cat: label1.cat, subcat: "N/A", confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 1} 
                }
            }
            else if (label2.cat === label3.cat) {
                if (label1.subcat === label2.subcat && label1.subcat === label3.subcat) {
                    return {cat: label2.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 3}
                }
                else if (label1.subcat === label2.subcat || label1.subcat === label3.subcat) {
                    return {cat: label2.cat, subcat: label1.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 2}
                }
                else if (label2.subcat === label3.subcat) {
                    return {cat: label2.cat, subcat: label2.subcat, confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 2} 
                }
                else {
                    return {cat: label2.cat, subcat: "N/A", confidence: conf, box_id: box_id, catMajority: 2, subcatMajority: 1} 
                }
            }
            else {
                return {cat: "N/A", subcat: "N/A", confidence: conf, box_id: box_id, catMajority: 1, subcatMajority: 1}
            }
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
                axios.get(self.$store.state.server_url+'/api/get-worker-annotations/',{
                params:{
                    doctype: self.$route.params.docType,
                    image_id: self.$store.state.image_order + self.$store.state.start_image_no
                }
                }).then(function(res){
                    self.worker_annots=res.data.workerannots;
                    console.log(res.data.workerannots);
                    /*
                    for (var i in res.data.workerannots) {
                        console.log("&&&&&", res.data.workerannots[i].user + " -- " + res.data.workerannots[i].annotations.length)
                    }*/
                    //var num_workers = res.data.workerannots.length
                    var majority = []
                    for (var i in res.data.workerannots[0].annotations) {
                        console.log(res.data.workerannots[0].annotations[i])
                        majority.push(self.majority_three(res.data.workerannots[0].annotations[i], res.data.workerannots[1].annotations[i], res.data.workerannots[2].annotations[i]))
                    }
                    self.majority_list = majority
                    console.log("MAJORITY -" , majority)
                });
                }
            }
        }
}
</script>

<style scoped>

.na.canbe{
  color: #ff5252 !important;
}
.exactly{
  color: #4caf50 !important;
}

.canbe{
    color: orange !important;
}

.datarow{
    height: 45px !important;
    margin: auto;
    line-height: 45px !important;
    border-bottom: 1px solid !important;
}
</style>

