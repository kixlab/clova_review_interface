<template>
    <v-col cols="12">
        <v-card>
            <v-card-title>
                <h4 style="marginRight: 10px;">Filter with MTurk ids --- </h4>
                <h5> <b style="color: red;">{{this.cnt_correct}}</b> out of <b style="color: blue">{{this.$store.getters.getImageBoxes.length}}</b> boxes 
                ({{(this.cnt_correct/this.$store.getters.getImageBoxes.length).toFixed(4)*100}}%) have majority labels equal to GT labels</h5>
            </v-card-title>
            <v-card-text>
                <v-container fluid>
                <v-row>
                <v-col v-for="(userannot, index) in worker_annots" :key="index">
                    <v-checkbox v-model="selected_workers" :label="userannot.user" :value="userannot.user">
                    </v-checkbox>
                </v-col>
                </v-row>
                </v-container>
            </v-card-text>
        </v-card>
        <v-card>
            <v-card-title style="border-bottom: 0px solid black; background-color: lightgrey;">
                <v-row>
                    <v-col cols="2">
                        <h4>Boxes</h4>
                    </v-col>
                    <v-col v-for="(userannot, index) in worker_annots.filter(v => selected_workers.indexOf(v.user) > -1)" :key="index">
                        <h4>Worker {{index+1}} - {{worker_annots.filter(v => selected_workers.indexOf(v.user) > -1)[index].user}}</h4>
                    </v-col>
                    <v-col cols="2">
                        <h4>Majority <br> (<span style="color: #4caf50">Green</span> if all same)</h4>
                    </v-col>
                    <v-col cols="2">
                        <h4>GT <br> (<span style="color: #4caf50">Green</span> if GT == majority)</h4>
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
                    <v-col v-for="(userannot, index) in worker_annots.filter(v => selected_workers.indexOf(v.user) > -1)" :key="index" style="border-right: 1px solid black; padding: 0px;">
                        <div v-for="box in userannot.annotations" :key="'annot-'+userannot.user+box.box_id" class="datarow">
                            <div v-bind:class="{exactly: box.confidence, na: (box.subcat=='N/A'), canbe: !box.confidence}"> 
                                    {{box.cat}}-{{box.subcat}} 
                            </div>
                        </div>
                        
                    </v-col>
                    <v-col cols="2" style="padding: 0px;">
                        <div v-for="box in majority_list" :key="'annot-'+box.box_id" class="datarow">
                            <div v-if="box.confidence && box.catMajority===3 && box.subcatMajority===3" style="color: #4caf50">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                            <div v-else-if="box.confidence===false && box.catMajority===3 && box.subcatMajority===3" style="color: orange">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                            <div v-else-if="box.cat==='N/A' || box.subcat==='N/A'" style="color: red">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                            <div v-else-if="box.catMajority===3 && box.subcatMajority===2" style="color: lightblue">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                            <div v-else-if="box.catMajority===2" style="color: blue">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                            <div v-else style="color: black">
                                {{box.cat}}-{{box.subcat}}
                            </div>
                        </div>
                    </v-col>
                    <v-col cols="2" style="padding: 0px; border-left: 1px solid black;">
                        <div v-for="(box, index) in image_box" :key="box.id" class="datarow">
                            <div v-if="majority_list[index].cat && gt_to_cat(box.GTlabel).cat">
                            <div v-if="majority_list[index].cat === gt_to_cat(box.GTlabel).cat && majority_list[index].subcat === gt_to_cat(box.GTlabel).subcat">
                                <div style="color: #4caf50">
                                    <b>{{gt_to_cat(box.GTlabel).cat}}-{{gt_to_cat(box.GTlabel).subcat}}</b>
                                </div>
                            </div>
                            <div v-else-if="majority_list[index].cat === gt_to_cat(box.GTlabel).cat">
                                <div style="color: orange">
                                    {{gt_to_cat(box.GTlabel).cat}}-{{gt_to_cat(box.GTlabel).subcat}}
                                </div>
                            </div>
                            <div v-else>
                                <div style="color: black">
                                    {{gt_to_cat(box.GTlabel).cat}}-{{gt_to_cat(box.GTlabel).subcat}}
                                </div>
                            </div>
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
            worker_annots: [{'user': null, 'annotations': []},{'user': null, 'annotations': []},{'user': null, 'annotations': []},{'user': null, 'annotations': []}],
            headers:[
                {
                text: 'Boxes',
                align: 'start',
                sortable: false, 
                value: ''
                }
            ],
            majority_list: [],
            cnt_correct: 0,
            selected_workers: [],
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
            var result = res.data.workerannots;
            //console.log("RESULT FROM SERVER ---", res.data.workerannots.map(v => v.user))
            self.worker_annots = result
            self.selected_workers = result.map(v => v.user).slice(0, 3)
            
            var majority = []
            for (var i in result[0].annotations) {
                //console.log(res.data.workerannots[0].annotations[i])
                var result_filter = result.filter(v => self.selected_workers.indexOf(v.user) > -1)
                majority.push(self.majority_three(result_filter[0].annotations[i], result_filter[1].annotations[i], result_filter[2].annotations[i]))
            }
            self.majority_list = majority

            var tempcnt = 0
            for (var j in majority) {
                if (self.gt_to_cat(self.image_box[j].GTlabel).cat === majority[j].cat && self.gt_to_cat(self.image_box[j].GTlabel).subcat === majority[j].subcat) {
                    tempcnt += 1
                }
            }
            self.cnt_correct = tempcnt
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
            if (label1 === undefined || label2 === undefined || label3 === undefined) {
                return {cat: "none", subcat: "none", box_id: label1.box_id}
            }
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
        },

        gt_to_cat(label) {
            var newlabel = label
            //newlabel = label.split(".")
            newlabel = newlabel === 'menu.num' ? 'menu.id' : newlabel
            newlabel = newlabel === 'menu.nm' ? 'menu.name' : newlabel
            newlabel = newlabel === 'menu.cnt' ? 'menu.count' : newlabel
            newlabel = (['menu.discountprice', 'menu.itemsubtotal', 'menu.vatyn', 'menu.etc', 
            'menu.sub_nm', 'menu.sub_unitprice', 'menu.sub_cnt', 'menu.sub_price', 'menu.sub_etc'].indexOf(newlabel) > -1) ? 'menu.n/a' : newlabel

            newlabel = newlabel === 'sub_total.subtotal_price' ? 'subtotal.price' : newlabel
            newlabel = newlabel === 'total.menutype_cnt' ? 'subtotal.menu count' : newlabel
            newlabel = newlabel === 'total.menuqty_cnt' ? 'subtotal.item count' : newlabel
            newlabel = newlabel === 'sub_total.service_price' ? 'subtotal.service charge' : newlabel
            newlabel = newlabel === 'sub_total.tax_price' ? 'subtotal.tax price' : newlabel
            newlabel = (['sub_total.discount_price', 'sub_total.othersvc_price', 'sub_total.etc'].indexOf(newlabel) > -1) ? 'sub_total.n/a': newlabel

            newlabel = newlabel === 'total.total_price' ? 'total.price' : newlabel
            newlabel = newlabel === 'total.total_etc' ? 'total.n/a' : newlabel

            newlabel = newlabel === 'total.cashprice' ? 'payment.cash' : newlabel
            newlabel = newlabel === 'total.changeprice' ? 'payment.change' : newlabel
            newlabel = newlabel === 'total.creditcardprice' ? 'payment.credit card' : newlabel
            newlabel = newlabel === 'total.emoneyprice' ? 'payment.n/a' : newlabel

            newlabel = newlabel.split(".")

            newlabel[0] = newlabel[0] === 'sub_total' ? 'subtotal' : newlabel[0]
            return {cat: newlabel[0], subcat: newlabel[1]}
        }
    },

    computed: {
        ...mapGetters(['image_no']),
    },

    watch: {
        image_no: {
            deep: true,
            handler() {
                const self=this;
                axios.get(self.$store.state.server_url+'/api/get-worker-annotations/',{
                params:{
                    doctype: self.$route.params.docType,
                    image_id: self.$store.state.image_order + self.$store.state.start_image_no
                }
                }).then(function(res){
                    var result = res.data.workerannots;
                    //console.log("RESULT FROM SERVER ---", res.data.workerannots.map(v => v.user))
                    self.worker_annots = result
                    self.selected_workers = result.map(v => v.user).slice(0, 3)
                    
                    var majority = []
                    for (var i in result[0].annotations) {
                        //console.log(res.data.workerannots[0].annotations[i])
                        var result_filter = result.filter(v => self.selected_workers.indexOf(v.user) > -1)
                        majority.push(self.majority_three(result_filter[0].annotations[i], result_filter[1].annotations[i], result_filter[2].annotations[i]))                 
                    }
                    self.majority_list = majority
                    
                    var tempcnt = 0
                    for (var j in majority) {
                        if (self.gt_to_cat(self.image_box[j].GTlabel).cat === majority[j].cat && self.gt_to_cat(self.image_box[j].GTlabel).subcat === majority[j].subcat) {
                            tempcnt += 1
                        }
                    }
                    self.cnt_correct = tempcnt
                });
            }
        },
        selected_workers: {
            deep: true,
            handler() {
                //console.log("CHANGEDDDD")
                const self = this;
                var majority = []
                var result_filter = self.worker_annots.filter(v => self.selected_workers.indexOf(v.user) > -1)
                for (var i in result_filter[0].annotations) {
                    //console.log(res.data.workerannots[0].annotations[i])
                    if (result_filter.length >= 3) {
                        majority.push(self.majority_three(result_filter[0].annotations[i], result_filter[1].annotations[i], result_filter[2].annotations[i]))
                        //console.log("NEW MAJORITY")
                    } else {
                        majority.push({cat: "none", subcat: "none", box_id: i})
                    } 
                }
                self.majority_list = majority
                
                var tempcnt = 0
                for (var j in majority) {
                    if (self.gt_to_cat(self.image_box[j].GTlabel).cat === majority[j].cat && self.gt_to_cat(self.image_box[j].GTlabel).subcat === majority[j].subcat) {
                        tempcnt += 1
                    }
                }
                self.cnt_correct = tempcnt
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

