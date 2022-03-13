<template>
    <v-container fluid fill-height style="padding: 0px;">
        <v-row class="fill-height" style="height: 100%;">
            <v-col cols="4" style="border: 1px solid red;">
                <h2>issues from annotators</h2>
                <div style="text-align:left;">
                    <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                    <v-list >
                    <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                        <v-list-item v-for="(category, idx) in na_issues" :key='category.pk' @click="selectIssue(category, idx)" dense style="border: 0px solid red; height: 20px">
                            <span><b>{{category.category}}</b> ({{na_issues.filter(v => v.category === category.category)[0].annotations.length}})</span>
                        </v-list-item>
                    </v-list-item-group>
                    </v-list>
                </div>

                <h3 style="margin-top: 20px">{{n_issues}} issues remaining<br/> <!--(need to be fixed according to # of annotations)--></h3>
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2 style="margin-bottom: 10px;">corresponding annotations w/ images</h2>
                <h3>*<span style="color: blue;">{{sel_cat}}</span>* category ({{selectedAnnotations.length}} issues selected)</h3>
                <v-btn x-small outlined @click="selectedAnnotations = []" :disabled="disabled" style="margin: 5px;">unselect all</v-btn>
                <div style="height: 60vh; border: 1px solid black; text-align: left; overflow-y: scroll;">
                        <v-row>
                            <v-col cols="auto" v-for="(annot, idx) in suggestions_show" :key="idx" style="margin: 0 10px">
                                <v-checkbox hide-details
                                    style="margin: 0;"
                                    v-model="selectedAnnotations"
                                    :label="idx+1+') Image #'+annot.image_no"
                                    :value="annot"
                                    @click.native.stop="check(annot)" 
                                ></v-checkbox>
                                <v-img :src="imageNo2Url(annot.image_no)" width="250">
                                    <div v-if="annot_boxes[annot.annotation_pk]">
                                        <div style="margin: 0; background: gray; color: white; font-size: 90%; text-align: center">
                                            {{annot_boxes[annot.annotation_pk].map(v=>v.text)}}
                                        </div>
                                        <div v-for="box in annot_boxes[annot.annotation_pk]" :key="box.id">
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
                <v-row justify="center" align="start" class="up_margin" no-gutters style="padding-top: 20px;">
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
                        <v-combobox :items="categories" label="Category" v-model="cat" :search-input.sync="search" dense solo style="width: 15%; margin-left: 5px"
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
    name: 'IssueResolution',
    components: {
        BoundingBox
    },
    data() {
        return {
            search: null,
            sel_category: 0, 

            
            headers: [
                { text: 'Category', align: 'start',  value: 'suggestion_cat', },
                { text: 'Suggested label', sortable: false, value: 'suggestion_text', },
                { text: '# workers', value: 'n_workers' },
                { text: '# images', value: 'n_images' },
                { text: '# boxes', value: 'n_boxes' },
            ],

            // 왼쪽 issue list에서  Selected category / subcat
            sel_cat: '',
            sel_subcat: '',

            // selection list 에 보여주는 것들
            categories: [],
            subcategories_all: [], 
            subcategories_show: [],

            // Show / hide save inputs
            clicked: '',

            // selection list에서 고른것 (api로 보내줌)
            cat: '',
            subcat: '',
            description: '' ,
            //selectedBoxes: [], // Not yet linked!
            //selectedBoxes_full: [],
            selectedAnnotations: [],

            na_issues:[],
            n_issues:0,
            suggestions_all: [],
            suggestions_show: [],

            done: false,

            annot_boxes: {},
        }
    },

    mounted: function () {
        const self = this;

        axios.get(self.$store.state.server_url + "/dashboard/get-na-reasons/",{
        params:{
          mturk_id: self.$store.state.mturk_id,
          doctype: self.$route.params.docType }

        })
        .then(function(res){
            window.alert('na issues loaded!')
            self.na_issues=res.data.na_reasons;
            var count=0
            for(var i=0;i<self.na_issues.length;i++){
                count+=self.na_issues[i]["annotations"].length;
            }
            self.n_issues=count;
            self.updateDistribution(res.data.distribution);
            //console.log(res.data.na_reasons);


        });

         axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
            params: {
                doctype: self.$route.params.docType
            }
        })
        .then(function(res){
            // First thing to show?
            //self.cats=res.data.cats;
            //self.subcats=res.data.subcats;
            //self.category=self.cats[0];

            // Show in selection list
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

        addAsNew() {
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        addToExisting() {
            this.clicked = this.clicked === 'addtoexisting' ? '' : 'addtoexisting'
        },

        saveLabels(dest) {
            const self = this;
            //console.log('call save with', self.cat, self.subcat, self.description)
            
            //issue handling 도 다르게 save
            axios.post(self.$store.state.server_url + '/dashboard/save-na-'+dest+'/', {
                expert_id: self.$store.state.mturk_id,
                annotation_pks:self.selectedAnnotations.map(v => v.annotation_pk),
                category:self.cat,
                subcategory:self.subcat,
                description: self.description,
                doctype: self.$route.params.docType
            }).then(function (res) {
                self.cat = ''
                self.subcat = ''
                self.selectedAnnotations = []
                self.clicked = ''

                self.na_issues=res.data.na_reasons;
                //console.log("AFTER SAVING",res.data)
                self.updateDistribution(res.data.distribution)
                
                self.suggestions_show = self.na_issues.filter(v => v.category === self.sel_cat)[0].annotations
                self.getFinalCat()

            })

            
        },

        // FIXME: 실제 쓸거
        selectIssue(selectedCategory, idx) {
            this.sel_cat = selectedCategory.category
            this.sel_category = idx

            this.suggestions_show = this.na_issues.filter(v => v.category === this.sel_cat)[0].annotations
            //console.log(this.suggestions_show)
            this.selectedAnnotations = []
            
        },

        // close to 에서 이렇게 고름
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;
            this.subcat_show_list = this.suggestions_all.filter(v => v.suggestion_cat === selectedCategory.cat).map(v => v.suggestion_subcat)
        },

        // n/a에서 이렇게 보여줌
        selectSuggestion(value) {
            //console.log('dd', value)

            this.sel_cat = value.suggestion_cat
            this.sel_subcat = value.suggestion_text

            this.suggestions_show = this.suggestions_all.filter(v => v.suggestion_cat === this.sel_cat && v.suggestion_text === this.sel_subcat)

            // 새로운 label 누를 때 다 초기화 시키기 위해..
            // this.selectedBoxes = []
            // this.selectedBoxes_full = []           
            
            this.selectedAnnotations = []
        },


        check() {
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
            
            const validData=json[0].valid_line.map(v => v.words).flat(1)

            //const newValidData = []
            for (var d in json[0].valid_line) {
                var word = json[0].valid_line[d].words
                var cat = json[0].valid_line[d].category
                for (var w in word) {
                    word[w]["GTlabel"] = cat
                }
            }
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
                
                return boxes
            })
        },

        async waitForJson(pk, no, box_id) {
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
        cat: {
            deep: true,
            handler(){
                this.subcategories_show = this.subcategories_all.filter(v => v.cat === this.cat).map(v => v.subcat)
            }
        },
        selectedBoxes: {
            deep: true,
            handler() {
            }
        },
    },

    computed: {
        disabled() {
            return this.selectedAnnotations.length === 0;
        },

        disableSave() {
            return this.subcat === '' || this.cat === '' || this.selectedAnnotations.length === 0;
        },

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