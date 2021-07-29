<template>
    <v-container fluid fill-height style="padding: 0">
        <v-row class="fill-height" style="height: 100vh;">
            <v-col cols="4" style="border: 1px solid red;">
                <h2>n/a suggestions</h2>
                <v-data-table
                    dense
                    :headers="headers"
                    :items="suggestions_all"
                    item-key="name"
                    class="elevation-1"
                    @click:row="selectSuggestion"
                >
                    <template v-slot:[`sugg.suggestion_full`]="{ sugg }">{{ sugg.suggestion_cat }} - {{ sugg.suggestion_text }}</template>
                </v-data-table>

                <h3 style="margin-top: 20px">{{suggestions_all.length}} suggestions remaining<br/> ( = {{suggestions_all.map(v => v.n_boxes).reduce((a, b) => a + b, 0)}} boxes )<!--(need to be fixed according to # of annotations)--></h3>
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2 style="margin-bottom: 10px;">corresponding annotations w/ images</h2>
                <h3>*<span style="color: blue;">{{sel_cat}} - {{sel_subcat}}</span>* selected</h3>
                <div style="height: 60vh; border: 1px solid black; text-align: left; overflow-y: scroll;">
                    
                    <div v-for="s in suggestions_show" :key="s.suggestion_pk">
                        <h4 class="suggestion">
                            Suggestion: <span style="color: blue;">{{ s.suggestion_cat }} - {{s.suggestion_text}}</span> 
                            
                        </h4>
                        <div style="margin-bottom: 10px">
                            <v-btn style="margin-left: 20px;" outlined x-small @click="selectAll(s.suggested_boxes, s.workers, s.suggestion_cat, s.suggestion_text)">select all</v-btn>
                            <v-btn style="margin-left: 10px;" outlined x-small @click="unselectAll(s.suggested_boxes, s.workers, s.suggestion_cat, s.suggestion_text)">unselect all</v-btn>
                        </div>
                        <v-row>
                            <v-col cols="6" v-for="(annot, idx) in s.suggested_boxes" :key="annot.annot_pk" style="margin: 0 10px">
                                <v-checkbox hide-details
                                    style="margin: 0;"
                                    v-model="selectedBoxes"
                                    :label="'Image #'+annot.image_no"
                                    :value="annot"
                                    @click="check(annot, s.workers[idx], s.suggestion_cat, s.suggestion_text)"
                                ></v-checkbox>
                                <!--{{imageNo2Json(annot.image_no)}}-->
                                <v-img :src="imageNo2Url(annot.image_no)" width="300">
                                    <div v-for="box in imageNo2Json(annot.image_no, annot.boxes_id, annot)" :key="box.box_id" >
                                        <div v-if="annot.boxes_id.indexOf(box.box_id) > -1">
                                            <bounding-box circle="yes" color="stroke:rgb(255, 105, 105); stroke-dasharray:0;" :box_info="box"/>
                                        </div>
                                        <div v-else>
                                            ddjksflj
                                        </div>
                                    </div>
                                    <span style="color: blue; background-color: white; margin-left: 1px;">Boxes: <b> {{annot.boxes_text}}</b></span>
                                </v-img>
                                {{done}}
                                <!--
                                #{{idx+1}} - {{annot.image_no}} & {{annot.boxes_id}} & {{annot.worker}}
                                -->
                                <div v-for="box in imageNo2Json(annot.image_no)" :key="box.box_id" >
                                    <div v-if="annot.boxes_id.indexOf(box.box_id) > -1">
                                        {{box.text}}
                                    </div>
                                    <div v-else>
                                    </div>
                                </div>
                            </v-col>
                            
                        </v-row>
                    </div>
                    
                </div>
                <v-row justify="center" align="start" class="up_margin" no-gutters style="padding-top: 20px;">
                    <v-btn :disabled="disabled" @click="approve()" color="indigo lighten-2" class="mr-4 white--text" depressed small>
                        Approve
                    </v-btn>
                    <v-btn :disabled="disabled" @click="addAsNew()" color="indigo lighten-2" class="mr-4 white--text" depressed small>
                        Add as new
                    </v-btn>
                    <v-btn :disabled="disabled" @click="addToExisting()" color="indigo lighten-2" class="mr-4 white--text" depressed small>
                        Add to existing
                    </v-btn>
                </v-row>
                <v-row justify="center">
                    <v-spacer/>
                    <template v-if="clicked === 'addasnew'">
                        <v-select
                            :items="categories" label="Category" v-model="cat" dense solo style="width: 15%; margin-left: 5px"
                        ></v-select>
                        <v-text-field
                            label="Sub-category" placeholder="Enter new subcategory" v-model="subcat" dense solo style="width: 20%; margin-left: 5px"
                        ></v-text-field>
                        <v-btn
                            small @click="saveLabels('new')" :disabled="disableSave" style="margin: 5px 0 0 7px;"
                        >save as new</v-btn>
                    </template>
                    <template v-if="clicked === 'addtoexisting'">
                        <v-select
                            :items="categories" label="Category" v-model="cat" dense solo style="width: 15%; margin-left: 5px"
                        ></v-select>
                        <v-select
                            :items="subcategories_show" label="Sub-category" v-model="subcat" dense solo style="width: 20%; margin-left: 5px"
                        ></v-select>
                        <v-btn
                            small @click="saveLabels('existing')" :disabled="disableSave" style="margin: 5px 0 0 7px;"
                        >save to existing</v-btn>
                    </template>
                    <v-spacer/>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
import {mapActions} from 'vuex';

export default {
    name: 'NaResolution',
    data() {
        return {
            headers: [
                { text: 'Category', align: 'start',  value: 'suggestion_cat', },
                { text: 'Suggested label', sortable: false, value: 'suggestion_text', },
                { text: '# workers', value: 'n_workers' },
                { text: '# images', value: 'n_images' },
                { text: '# boxes', value: 'n_boxes' },
            ],

            sel_cat: '',
            sel_subcat: '',

            // Save selection list
            categories: [],
            subcategories_all: [], 
            subcategories_show: [],

            // Show / hide save inputs
            clicked: '',

            // Selected data to save
            cat: '',
            subcat: '',
            selectedBoxes: [], // Not yet linked!
            selectedBoxes_full: [],

            suggestions_all: [],
            suggestions_show: [],

            done: false,
        }
    },

    mounted: function () {
        const self = this;

        axios.get(self.$store.state.server_url + "/dashboard/get-na-suggestions/",{
        params:{
          mturk_id: self.$store.state.mturk_id }

        })
        .then(function(res){
            console.log(res.data);
            window.alert('na suggestions loaded!')
            self.suggestions_all=res.data.na_suggestions;
        })


        axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
        })
        .then(function(res){
            self.categories = res.data.cats.map(v => v.cat).filter(v => v !== 'n/a')
            self.subcategories_all = res.data.subcats.filter( v => v.subcat !== 'n/a' && v.cat !== 'n/a')
        })
    },


    methods: {
        ...mapActions(['updateDistribution']),
        
        approve() {
            const self = this;
            //console.log('approve clicked')

            var selectedBoxes_final = []
            for (var b in self.selectedBoxes_full) {
                var temp = self.selectedBoxes_full[b]
                temp.cat = self.selectedBoxes_full[b].suggested_cat
                temp.subcat = self.selectedBoxes_full[b].suggested_subcat
                selectedBoxes_final.push(temp)
            }
            console.log({expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final})

            axios.post(self.$store.state.server_url + '/dashboard/save-na-approve/', {
                expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final
            }).then(function (res) {
                //console.log(res)
                self.selectedBoxes = []
                self.selectedBoxes_full = []

                self.suggestions_all=res.data.na_suggestions;
                self.updateDistribution(res.data.distribution)
            })
        },

        addAsNew() {
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        addToExisting() {
            this.clicked = this.clicked === 'addtoexisting' ? '' : 'addtoexisting'
        },

        saveLabels(dest) {
            const self = this;
            //console.log(this.cat, "-", this.subcat)
            var selectedBoxes_final = []
            for (var b in self.selectedBoxes_full) {
                var temp = self.selectedBoxes_full[b]
                temp.cat = self.cat
                temp.subcat = self.subcat
                selectedBoxes_final.push(temp)
            }
            console.log({expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final})

            axios.post(self.$store.state.server_url + '/dashboard/save-na-'+dest+'/', {
                expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final
            }).then(function (res) {
                //console.log(res)
                self.cat = ''
                self.subcat = ''
                self.selectedBoxes = []
                self.selectedBoxes_full = []

                self.clicked = ''

                self.suggestions_all=res.data.na_suggestions;
                self.updateDistribution(res.data.distribution)
            })

            
        },

        selectSuggestion(value) {
            console.log('dd', value)

            this.sel_cat = value.suggestion_cat
            this.sel_subcat = value.suggestion_text

            this.suggestions_show = this.suggestions_all.filter(v => v.suggestion_cat === this.sel_cat && v.suggestion_text === this.sel_subcat)

            console.log(this.suggestions_show)
            // 새로운 label 누를 때 다 초기화 시키기 위해..
            this.selectedBoxes = []
            this.selectedBoxes_full = []            
        },

        selectAll(annots, workers, sugg_cat, sugg_subcat) {
            var tempbox = this.selectedBoxes
            var tempbox_full = this.selectedBoxes_full
            for (var a in annots) {
                tempbox.push(annots[a])
                annots[a].worker_id = workers[a]
                annots[a].suggested_cat = sugg_cat
                annots[a].suggested_subcat = sugg_subcat
                annots[a].cat = this.sel_cat
                annots[a].subcat = this.sel_subcat
                tempbox_full.push(annots[a])
            }
        },

        unselectAll(annots, workers, sugg_cat, sugg_subcat) {
            var tempbox = this.selectedBoxes
            var tempbox_full = this.selectedBoxes_full
            for (var a in annots) {
                tempbox.splice(tempbox.indexOf(annots[a]), 1)
                annots[a].worker_id = workers[a]
                annots[a].suggested_cat = sugg_cat
                annots[a].suggested_subcat = sugg_subcat
                annots[a].cat = this.sel_cat
                annots[a].subcat = this.sel_subcat
                tempbox_full.splice(tempbox_full.indexOf(annots[a]))
            }
        },

        check(annot, worker, sugg_cat, sugg_subcat) {
            var tempbox_full = this.selectedBoxes_full
            if (this.selectedBoxes.indexOf(annot) > -1) {
                annot.worker_id = worker
                annot.suggested_cat = sugg_cat
                annot.suggested_subcat = sugg_subcat
                annot.cat = this.sel_cat
                annot.subcat = this.sel_subcat
                tempbox_full.push(annot)
            }
            else {
                annot.worker_id = worker
                annot.cat = this.sel_cat
                annot.subcat = this.sel_subcat
                tempbox_full.splice(tempbox_full.indexOf(annot))
            }
        },


        setImageBoxes(json) {
            //console.log("NEW JSON --------\n" , json)
            const img_w = json[0].meta === undefined ? json[0].image_size.width : (json[0].meta.image_size === undefined? json[0].meta.imageSize.width:json[0].meta.image_size.width)
            const img_h = json[0].meta === undefined ? json[0].image_size.height : (json[0].meta.image_size === undefined? json[0].meta.imageSize.height:json[0].meta.image_size.height)
            var ratio = 1
            var padding_x = 0
            var padding_y = 0
            if (img_w/json[1] >= img_h/json[2]) {
                ratio = img_w/json[1]
                padding_y = 0//(json[2]-(img_h/ratio))/2
            } else {
                ratio = img_h/json[2]
                padding_x = (json[1]-(img_w/ratio))/2
            }

            //commit('setImageRatio', ratio)
            
            const validData=json[0].valid_line.map(v => v.words).flat(1)

            //const newValidData = []
            for (var d in json[0].valid_line) {
                var word = json[0].valid_line[d].words
                var cat = json[0].valid_line[d].category
                for (var w in word) {
                    word[w]["GTlabel"] = cat
                    //newValidData.push(word[w])
                }
            }
            //console.log("VALIDDATA", validData)
            const processedData = validData.map(function(i, idx) {
                return {box_id: idx,
                        text: i.text,
                        x_pos: i.quad.x1/ratio+padding_x, 
                        y_pos: i.quad.y1/ratio+padding_y, 
                        x_len: (i.quad.x2-i.quad.x1)/ratio, 
                        y_len: (i.quad.y3-i.quad.y2)/ratio, 
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.quad.x1, y1: i.quad.y1, x2: i.quad.x2, y2: i.quad.y2, y3: i.quad.y3},
                        label: "",
                        GTlabel: i.GTlabel,
                    }
            })
            return processedData
        },

        imageNo2Url(no) {
            var docType= 'receipt'
            var three_digit_id = ("00" + no).slice(-3);
            return this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
        },

        imageNo2Json(no, box_id, annot) {
            const self = this;
            var docType= 'receipt'
            var three_digit_id = ("00" + no).slice(-3);
            const json_url = this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
            
            return axios.get(json_url).then(function(res) {
                var json = res.data;
                var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
                var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height)

                const width = 250;//cont_pos.right-cont_pos.left
                //const height = cont_pos.bottom-cont_pos.top

                const resbox = self.setImageBoxes([json, width, width*img_height/img_width, true]);
                //self.original_box = json;

                console.log(resbox)
                //self.$forceUpdate();
                self.done = ''
                //console.log(box_id)
                var texts = []
                if (resbox && box_id) {
                    for (var b in resbox) {
                        if (box_id.indexOf(resbox[b].box_id) > -1) {
                            //console.log(resbox[b].text)
                            texts.push(resbox[b].text)
                        }
                    }
                }
                if (annot) {
                    annot.boxes_text = texts
                }


                return resbox
            })
        },


    },

    watch: {
        cat: {
            deep: true,
            handler(){
                this.subcategories_show = this.subcategories_all.filter(v => v.cat === this.cat).map(v => v.subcat)
            }
        },
        selectedBoxes: {
            deep: true,
            handler() {
                //console.log(this.selectedBoxes)
            }
        },
    },

    computed: {
        disabled() {
            return this.selectedBoxes_full.length === 0;
        },

        disableSave() {
            return this.subcat === '' || this.cat === ''
        }
    }

}
</script>

<style scoped>
h2 {
    margin: 10px 0 20px;
}

.suggestion {
    margin: 15px 0 5px 15px;
}
</style>