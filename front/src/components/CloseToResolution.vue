<template>
    <v-container fluid fill-height style="padding: 0">
        <v-row class="fill-height" style="height: 85vh;">
            <v-col cols="4" style="border: 1px solid red;"> 
                <h2>label set</h2>
                <v-row dense>
                    <v-col :cols="4" style="text-align:left;">
                        <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                        <v-list >
                        <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                            <v-list-item v-for="category in close_to_suggestions" :key='category.pk' @click="selectCategory(category)">
                                <b>{{category.cat}}</b>
                            </v-list-item>
                        </v-list-item-group>
                        </v-list>
                    </v-col>

                    <v-col :cols="8" style="text-align:left;">
                        <h4 style="background-color: #3F51B5; color: #E8EAF6">Sub-category</h4>
                        <v-list>
                        <v-list-item-group v-model="sel_subcategory" color="indigo"> 
                            <div v-for="subcat in sel_category.subcat" :key="subcat.pk" >
                                <v-list-item v-if="subcat_show_list.indexOf(subcat.subcat) > -1" @click="selectSubcat(subcat)">
                                    <span class='subcat-div'>
                                        <b>{{subcat.subcat}}</b>: <span style="color: gray">{{subcat.description}}</span>
                                    </span>
                                </v-list-item>
                                
                            </div>
                            <template v-if="subcat_show_list.length === 0">
                                <span style="margin: 5px 5px 0 0; padding: 5px 0">
                                    No suggestion available for "{{category.cat}}" category
                                </span>
                            </template>
                        </v-list-item-group>
                        </v-list>
                    </v-col>
                </v-row>
                
                <h3 style="margin-top: 20px">{{suggestions_all.length}} suggestions remaining <br/> ( = {{suggestions_all.map(v => v.n_boxes).reduce((a, b) => a + b, 0)}} boxes )<!--(need to be fixed according to # of annotations)--></h3>
                
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2 style="margin-bottom: 10px;">corresponding annotations w/ images</h2>
                <h3>*<span style="color: blue;">{{sel_cat}} - {{sel_subcat}}</span>* selected</h3>
                <div style="height: 60vh; border: 1px solid black; text-align: left; overflow-y: scroll" >
                    
                    <div v-for="s in sel_subcategory.suggestions" :key="s.suggestion_pk" style="border: 1px solid grey; padding-bottom: 5px; text-align: center;">
                        <h4 class="suggestion">
                            Suggestion: <span style="color: blue;">{{s.suggestion_cat}} - {{s.suggestion_text}}</span> 
                            
                        </h4>
                        <div style="margin-bottom: 10px">
                            <v-btn style="margin-left: 20px;" outlined x-small @click="selectAll(s.suggested_boxes, s.workers, s.suggestion_cat, s.suggestion_text)">select all</v-btn>
                            <v-btn style="margin-left: 10px;" outlined x-small @click="unselectAll(s.suggested_boxes, s.workers, s.suggestion_cat, s.suggestion_text)">unselect all</v-btn>
                        </div>
                        <v-row>
                            <v-col cols="auto" v-for="(annot, idx) in s.suggested_boxes" :key="annot.annot_pk" style="margin: 0 10px">
                                <v-checkbox hide-details
                                    style="margin: 0;"
                                    v-model="selectedBoxes"
                                    :label="'Image #'+annot.image_no"
                                    :value="annot"
                                    @click="check(annot, s.workers[idx], s.suggestion_cat, s.suggestion_text)"
                                ></v-checkbox>
                                <!--{{imageNo2Json(annot.image_no)}}-->
                                <v-img :src="imageNo2Url(annot.image_no)" width="250">
                                    <div v-if="annot_boxes[annot.image_no]">
                                        <div style="margin: 0; background: gray; color: white; font-size: 90%">{{annot_boxes[annot.image_no].map(v=>v.text)}}</div>
                                        <div v-for="box in annot_boxes[annot.image_no]" :key="box.id"><!--{{annot_boxes[annot.issue_pk].length}}-->
                                            <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                                        </div>
                                    </div>
                                    <div style="opacity: 0.0;">{{waitForJson(annot.image_no, annot.boxes_id)}}</div>
                                </v-img>
                            </v-col>
                            
                        </v-row>
                    </div>

                    <!-- For cases where there are no suggestions -->
                    <div v-if="suggestions_show.length === 0 && sel_cat === '' && sel_subcat === ''">
                        <h4 class="suggestion">Please select a label from left to see <br/>"Close to" annotations & suggestions</h4>
                    </div>
                    <div v-else-if="suggestions_show.length === 0 && sel_cat !== '' && sel_subcat !== ''"> 
                        <h4 class="suggestion">No suggested label for this label</h4>
                    </div>

                    <!--
                    <div v-for="s in suggestions_show" :key="s.suggestion_pk+'/'">
                        {{s}} //
                    </div>
                    -->
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
                    <v-btn :disabled="disabled" @click="ignore()" color="error" class="mr-4 white--text" depressed small>
                        Ignore
                    </v-btn>
                </v-row>
                <v-row justify="center">
                    <v-spacer/>
                    <template v-if="clicked === 'addasnew'">
                        <v-combobox
                            :items="categories" label="Category" v-model="cat" dense solo style="width: 15%; margin-left: 5px" :search-input.sync="search"
                        ></v-combobox>
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
import BoundingBox from '@/components/BoundingBox.vue'
import {mapActions} from 'vuex';


export default {
    name: 'CloseToResolution',
    components: {
        BoundingBox,
    },
    data() {
        return {
            cats: ['menu', 'subtotal', 'total', 'payment'],
            subcats: [],
            category: '',
            subcategory: '',

            subcat_show_list: [],

            sel_category: 0, 
            sel_subcategory: null,

            sel_cat: '',
            sel_subcat: '',


            search: null,



            // Save selection list
            categories: [],
            
            // Show / hide save inputs
            clicked: '',

            // Selected data to save
            cat: '',
            subcat: '',
            selectedBoxes: [], 
            selectedBoxes_full: [],

            suggestions_all:[],
            suggestions_show: [],

            done: false,

            annot_boxes: {},
        }
    },

    mounted: function() {
        const self = this;
        axios.get(self.$store.state.server_url + "/dashboard/get-closeto-suggestions/",{
        params:{
          mturk_id: self.$store.state.mturk_id, doctype: self.$route.params.docType }

        })
        .then(function(res){
            console.log(res.data);
            self.close_to_suggestions=res.data.close_to_suggestions;

            self.suggestions_all=res.data.close_to_suggestions;
            self.sel_category = 0;
            self.subcat_show_list = self.suggestions_all.filter(v => v.suggestion_cat === self.categories[0]).map(v => v.suggestion_subcat)
        })

        axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
            params: {
                doctype: self.$route.params.docType
            }
        })
        .then(function(res){
            self.cats=res.data.cats;
            self.subcats=res.data.subcats;
            self.category=self.cats[0];

            self.categories = res.data.cats.map(v => v.cat).filter(v => v !== 'n/a')
            self.sel_category = 0;
        })
    },

    methods: {
        ...mapActions(['updateDistribution']),

        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;


            this.subcat_show_list = this.suggestions_all.filter(v => v.suggestion_cat === selectedCategory.cat).map(v => v.suggestion_subcat)
        },

        selectSubcat(cat) {
            //console.log(cat.cat, cat.subcat, '-', cat.description)
            this.sel_cat = cat.cat
            this.sel_subcat = cat.subcat

            this.suggestions_show = this.suggestions_all.filter(v => v.suggestion_cat === this.sel_cat && v.suggestion_subcat === this.sel_subcat)
            
            // 새로운 label 누를 때 다 초기화 시키기 위해..
            this.selectedBoxes = []
            this.selectedBoxes_full = []
        },



        approve() {
            //console.log('approve clicked')
            const self = this;
            
            var selectedBoxes_final = []
            for (var b in self.selectedBoxes_full) {
                var temp = self.selectedBoxes_full[b]
                temp.cat = self.selectedBoxes_full[b].suggested_cat
                temp.subcat = self.selectedBoxes_full[b].suggested_subcat
                selectedBoxes_final.push(temp)
            }
            console.log({expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final})

            axios.post(self.$store.state.server_url + '/dashboard/save-close-to-approve/', {
                expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final, 
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res.data)
                self.selectedBoxes = []
                self.selectedBoxes_full = []

                self.suggestions_all=res.data.close_to_suggestions;
                self.updateDistribution(res.data.distribution)

                self.suggestions_show = self.suggestions_all.filter(v => v.suggestion_cat === self.sel_cat && v.suggestion_text === self.sel_subcat)
            })
        },

        addAsNew() {
            //console.log('add as new clicked')
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        addToExisting() {
            this.clicked = this.clicked === 'addtoexisting' ? '' : 'addtoexisting'
        },

        ignore() {
            const self = this;

            //console.log('ignore clicked')
            console.log({expert_id: self.$store.state.mturk_id, saved_boxes: self.selectedBoxes_full})
            
            axios.post(this.$store.state.server_url + '/dashboard/save-close-to-ignore/', {
                expert_id: this.$store.state.mturk_id, saved_boxes: self.selectedBoxes_full,
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res)
                self.selectedBoxes = []
                self.selectedBoxes_full = []

                self.suggestions_all=res.data.close_to_suggestions;
                self.updateDistribution(res.data.distribution)

                self.suggestions_show = self.suggestions_all.filter(v => v.suggestion_cat === self.sel_cat && v.suggestion_text === self.sel_subcat)
            })
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

            axios.post(self.$store.state.server_url + '/dashboard/save-close-to-'+dest+'/', {
                expert_id: self.$store.state.mturk_id, saved_boxes: selectedBoxes_final,
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res)
                self.cat = ''
                self.subcat = ''
                self.selectedBoxes = []
                self.selectedBoxes_full = []

                self.clicked = ''

                self.suggestions_all=res.data.close_to_suggestions;
                self.updateDistribution(res.data.distribution)

                self.suggestions_show = self.suggestions_all.filter(v => v.suggestion_cat === self.sel_cat && v.suggestion_text === self.sel_subcat)
            })

            
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

        imageNo2Json(no, box_id) {
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

                self.done = ''
                var boxes = []

                boxes = resbox.filter(v => box_id.includes(v.box_id))
                //var texts = boxes.map(v => v.text)


                return boxes
            })
        },

        async waitForJson(no, box_id) {
            const response = await this.imageNo2Json(no, box_id)
            if (this.annot_boxes[no] === undefined) {
                this.$set(this.annot_boxes, no, response)
                //console.log("ANNOT BOXES", this.annot_boxes)
            }
            return response
        },


    },

    watch: {
        selectedBoxes: {
            deep: true,
            handler() {
                //console.log(this.selectedBoxes)
            }
        },
        selectedBoxes_full: {
            deep: true,
            handler() {
                //console.log("full", this.selectedBoxes_full)
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