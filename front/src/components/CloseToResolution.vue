<template>
    <v-container fluid fill-height class="align-start" style="padding: 0; margin-top: 0px;">
        <v-row class="fill-height" style="height: 85vh; margin-top: 0px;">
            <v-col cols="4" style="border: 1px solid red; padding: 0"> 
                <h2>label set</h2>
                
                <v-row dense>
                    <v-col :cols="4" style="text-align:left;">
                        <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                        <v-list >
                        <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                            <v-list-item v-for="category in cats.filter(v => v.cat !== 'n/a')" :key='category.pk' @click="selectCategory(category)">
                                <b>{{category.cat}}</b>
                            </v-list-item>
                        </v-list-item-group>
                        </v-list>
                    </v-col>

                    <v-col :cols="8" style="text-align:left;">
                        <h4 style="background-color: #3F51B5; color: #E8EAF6">Sub-category</h4>
                        <v-list>
                        <v-list-item-group v-model="sel_subcategory" color="indigo"> 
                           
                                
                                <v-list-item v-for="sugg in subcat_show_list" :key="sugg.pk" @click="selectSubcat(sugg)">
                                    <span class='subcat-div'>
                                        <b>{{sugg.subcat}}</b>: <span style="color: gray">{{sugg.subcat_description}}</span> ({{sugg.suggestions.length}} | {{sugg.suggestions.map(v => v.annotations).flat(1).length}})
                                    </span>
                                </v-list-item>
                                
                            <template v-if="subcat_show_list === undefined">
                                <span style="margin: 5px 5px 0 0; padding: 5px 0">
                                    No suggestion available for "{{category.cat}}" category
                                </span>
                            </template>
                        </v-list-item-group>
                        </v-list>
                    </v-col>
                </v-row>
                
                <h3 style="margin-top: 20px">{{suggestions_all.map(v => v.subcat).flat(1).map(v => v.suggestions).flat(1).length}} suggestions remaining <br/> ( = {{suggestions_all.map(v => v.subcat).flat(1).map(v => v.suggestions).flat(1).map(v => v.annotations).flat(1).length}} annotations )<!--(need to be fixed according to # of annotations)--></h3>
                
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2 style="margin-bottom: 10px;">corresponding annotations w/ images</h2>
                <h3>Suggestions from *<span style="color: blue;">{{sel_cat}} - {{sel_subcat}}</span>* <span style="font-size: 80%">(total {{suggestions_show.length}} suggestions)</span></h3>
                <div style="height: 60vh; border: 1px solid black; text-align: left; overflow-y: scroll" >
                    
                    <div v-for="s in suggestions_show" :key="s.suggestion_pk" >
                        <h4 class="suggestion">
                            Suggestion: <span style="color: blue;">{{s.suggestion_cat}} - {{s.suggested_subcat}}</span><br/> ({{s.n_annotations}} annotations total, {{selectedBoxes.length}} selected) 
                            
                        </h4>
                        <div style="margin-bottom: 10px">
                            <v-btn style="margin-left: 20px;" outlined x-small @click="selectAll(s.annotations, s.suggested_subcat)">select all</v-btn>
                            <v-btn style="margin-left: 10px;" outlined x-small @click="unselectAll(s.annotation)">unselect all</v-btn>
                        </div>
                        <v-row>
                            <v-col cols="auto" v-for="(annot) in s.annotations" :key="annot.annot_pk" style="margin: 0 10px">
                                <v-checkbox hide-details
                                    style="margin: 0;"
                                    v-model="selectedBoxes"
                                    :label="'Image #'+annot.image_no"
                                    :value="annot"
                                    @click="check(annot, s.suggested_subcat)"
                                ></v-checkbox>
                                <!--{{imageNo2Json(annot.image_no)}}-->
                                <div v-if="annot_boxes[annot.annotation_pk]">
                                    <div style="margin: 0; background: gray; color: white; font-size: 90%; text-align: center; width: 250px;">
                                        {{annot_boxes[annot.annotation_pk].map(v=>v.text)}}
                                    </div>
                                </div>
                                <v-img :src="imageNo2Url(annot.image_no)" width="250">
                                    <div v-if="annot_boxes[annot.annotation_pk]">
                                        <div v-for="box in annot_boxes[annot.annotation_pk]" :key="box.id"><!--{{annot_boxes[annot.issue_pk].length}}-->
                                            <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                                        </div>
                                    </div>
                                    <div style="opacity: 0.0;">{{waitForJson(annot.annotation_pk, annot.image_no, annot.boxes_id)}}</div>
                                </v-img>
                                <div style="width: 250px;">
                                Reason: {{annot.reason}}
                                </div>
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

            sugg_subcat: '',


            search: null,



            // Save selection list
            categories: [],
            subcategories_all: [], 
            subcategories_show: [],
            
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
            //console.log("CLOSE TO ---", res.data);
            self.suggestions_all=res.data.close_to_suggestions;
            self.sel_category = 0;
            self.subcat_show_list = self.suggestions_all.filter(v => v.cat === self.categories[0]).map(v => v.subcat)[0]
            //console.log(self.subcat_show_list)
        })

        axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
            params: {
                mturk_id: self.$store.state.mturk_id, 
                doctype: self.$route.params.docType
            }
        })
        .then(function(res){
            self.cats=res.data.cats;
            self.subcats=res.data.subcats;
            self.category=self.cats[0];
            

            self.categories = res.data.cats.map(v => v.cat).filter(v => v !== 'n/a')
            self.subcategories_all = res.data.subcats
            self.sel_category = 0;
        })

        // final label set 이 바뀌면 바뀐 label set 을 가지고 있기 위해
        self.$store.subscribeAction({after: (action) => {
            if (action.type === 'updateDistribution') {
                self.getFinalCat()
            }
        }})
    },

    methods: {
        ...mapActions(['updateDistribution']),

        getFinalCat() {
            const self = this;
            axios.get(self.$store.state.server_url + "/dashboard/get-final-cats",{
                params: {
                    doctype: self.$route.params.docType,
                    mturk_id: self.$store.state.mturk_id,
                }
            })
            .then(function(res){
                //console.log(res.data)
                self.categories = res.data.final_cats.map(v => v.cat).filter(v => v !== 'n/a')
                self.subcategories_all = res.data.final_subcats
            }) 
        },

        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;

            this.subcat_show_list = this.suggestions_all.filter(v => v.cat === selectedCategory.cat).map(v => v.subcat)[0]
            //console.log(this.subcat_show_list)
        },

        selectSubcat(cat) {
            this.sel_cat = this.category.cat
            this.sel_subcat = cat.subcat

            //console.log(this.category.cat, '-', cat.subcat)

            this.suggestions_show = cat.suggestions
            
            // 새로운 label 누를 때 다 초기화 시키기 위해..
            this.selectedBoxes = []
        },



        approve() {
            const self = this;
                axios.post(self.$store.state.server_url + '/dashboard/save-close-to-approve/', {
                mturk_id: self.$store.state.mturk_id, 
                annotation_pks:self.selectedBoxes.map(v => ({annotation_pk: v.annotation_pk, sugg_subcat: v.suggested_subcategory})),
                category:self.sel_cat,
                description: '',
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res.data)
                self.selectedBoxes = []

                self.suggestions_all=res.data.close_to_suggestions;
                self.subcat_show_list = self.suggestions_all.filter(v => v.cat === self.sel_cat).map(v => v.subcat)[0]

                self.updateDistribution(res.data.distribution)

                self.suggestions_show = self.subcat_show_list === undefined? [] :(self.subcat_show_list.length===0? []: self.subcat_show_list.filter(v => v.subcat === self.sel_subcat)[0].suggestions)


                self.getFinalCat()

            })
            
        },

        addAsNew() {
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        addToExisting() {
            this.clicked = this.clicked === 'addtoexisting' ? '' : 'addtoexisting'
        },

        ignore() {
            const self = this;

            //console.log('ignore clicked')

            /*
            console.log({mturk_id: self.$store.state.mturk_id, 
                annotation_pks:self.selectedBoxes.map(v => v.annotation_pk),
                category:self.sel_cat,
                subcategory:self.sel_subcat,
                description: '',//self.description,
                doctype: self.$route.params.docType
            })
            */
            
            axios.post(this.$store.state.server_url + '/dashboard/save-close-to-ignore/', {
                annotation_pks:self.selectedBoxes.map(v => v.annotation_pk),
                mturk_id: self.$store.state.mturk_id, 
                category:self.sel_cat,
                subcategory:self.sel_subcat,
                description: '',//self.description,
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res.data)
                self.selectedBoxes = []

                self.suggestions_all=res.data.close_to_suggestions;
                self.subcat_show_list = self.suggestions_all.filter(v => v.cat === self.sel_cat).map(v => v.subcat)[0]

                self.updateDistribution(res.data.distribution)

                self.suggestions_show = self.subcat_show_list === undefined? [] : (self.subcat_show_list.length===0? []: self.subcat_show_list.filter(v => v.subcat === self.sel_subcat)[0].suggestions)


                self.getFinalCat()

            })
        },


        saveLabels(dest) {
            const self = this;
            //console.log(this.cat, "-", this.subcat)
            /*
            console.log({expert_id: self.$store.state.mturk_id, 
                annotation_pks:self.selectedBoxes.map(v => v.annotation_pk),
                category:self.sel_cat,
                subcategory:self.sel_subcat,
                description: '',//self.description,
                doctype: self.$route.params.docType
            })
            */

            axios.post(self.$store.state.server_url + '/dashboard/save-close-to-'+dest+'/', {
                mturk_id: self.$store.state.mturk_id, 
                annotation_pks:self.selectedBoxes.map(v => v.annotation_pk),
                category:self.cat,
                subcategory:self.subcat,
                description: '',//self.description,
                doctype: self.$route.params.docType
            }).then(function (res) {
                //console.log(res.data)
                self.cat = ''
                self.subcat = ''
                self.selectedBoxes = []

                self.clicked = ''

                self.suggestions_all=res.data.close_to_suggestions;
                self.updateDistribution(res.data.distribution)

                self.subcat_show_list = self.suggestions_all.filter(v => v.cat === self.sel_cat).map(v => v.subcat)[0]
                self.suggestions_show = self.subcat_show_list === undefined? [] : (self.subcat_show_list.length===0? []: self.subcat_show_list.filter(v => v.subcat === self.sel_subcat)[0].suggestions)


                self.getFinalCat()
            })

            
        },

        selectAll(annots, sugg) {
            this.selectedBoxes = annots
            this.sugg_subcat = sugg
        },

        unselectAll() {
            this.selectedBoxes = []
            this.sugg_subcat = ''
        },

        check(annot, sugg_subcat) {
            this.sugg_subcat = sugg_subcat
            //console.log(annot)

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
            if(json[0].valid_line==undefined){
            const validData = (json[0]['boxes']===undefined? json[0]['words']:json[0]['boxes']);
            const processedData = validData.map(function(i) {
                if(i.box_id==undefined){
                    return {
                        box_id: i.id, 
                        text:i.text, 
                        x_pos: Math.min(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0])/ratio + padding_x, 
                        y_pos: Math.min(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1])/ratio + padding_y,
                        x_len: (Math.max(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0]) - Math.min(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0]))/ratio, 
                        y_len: (Math.max(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1])-Math.min(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1]))/ratio,
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.boundingBox[0][0], y1: i.boundingBox[0][1], x2: i.boundingBox[1][0], y2: i.boundingBox[0][1], y3: i.boundingBox[2][1]},
                        label: ""
                    }
                }else{
                    return {
                        box_id: i.box_id,
                        text: i.text,
                        x_pos: i.x[0]/ratio+padding_x, 
                        y_pos: i.y[0]/ratio+padding_y, 
                        x_len: (i.x[1]-i.x[0])/ratio, 
                        y_len: (i.y[2]-i.y[0])/ratio,
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.x[0], y1: i.y[0], x2: i.x[1], y2: i.y[2], y3: i.y[3]},
                        label: ""}
                }
            
            })
            return processedData
            }

            else {
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
            }
        },

        imageNo2Url(no) {
            var docType= this.$route.params.docType
            var three_digit_id = ("00" + no).slice(-3);
            return this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
        },
        imageNo2Json(no, box_id) {
            const self = this;
            var docType= this.$route.params.docType
            var three_digit_id = ("00" + no).slice(-3);
            const json_url = this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
            
            return axios.get(json_url).then(function(res) {
                var json = res.data;
                var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
                var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height)
                const width = 250;
                const resbox = self.setImageBoxes([json, width, width*img_height/img_width, true]);

                self.done = ''
                
                var boxes = []
                boxes = resbox.filter(v => JSON.parse(box_id).includes(v.box_id))
                //var texts = boxes.map(v => v.text)
                
                return boxes
            })
        },
        async waitForJson(pk, no, box_id) {
            //console.log(json)
            //console.log(no, box_id)
            const response = await this.imageNo2Json(no, box_id)
            //console.log(response)
            if (this.annot_boxes[pk] === undefined) {
                this.$set(this.annot_boxes, pk, response)
                //console.log("ANNOTBOXES", Object.keys(this.annot_boxes).length)
            }
            return response
        },


    },

    watch: {
        selectedBoxes: {
            deep: true,
            handler() {
                //console.log(this.selectedBoxes)
                if (this.selectedBoxes.length === 0) {
                    this.sugg_subcat = ''
                }
            }
        },
        selectedBoxes_full: {
            deep: true,
            handler() {
                //console.log("full", this.selectedBoxes_full)
            }
        },
        cat: {
            deep: true,
            handler(){
                this.subcategories_show = this.subcategories_all.filter(v => v.cat === this.cat).map(v => v.subcat)
            }
        },
    },

    computed: {
        disabled() {
            return this.selectedBoxes.length === 0;
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