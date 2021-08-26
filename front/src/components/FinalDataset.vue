<template>
    <v-container fluid fill-height >
        <v-row>
            <v-col style="padding: 0;">
                <template v-if="distribution.length > 0">
                <h3>{{distribution.map(v => v.subcat_distn.length).reduce((a, b) => a+b)}} labels & </h3>
                <h3>{{distribution.map(v => v.cat_count).reduce((a, b) => a+b)}} boxes in total</h3>
                </template>
            </v-col>
        </v-row>
        <v-row> 
            <v-col cols="12" style="padding: 0px;">
            <v-switch hide-details style="margin-left: 10px"
            v-model="sort_bool" 
            :label="`${sort_bool? 'Sub-categories sorted': 'Sub-categories not sorted'}`"
            ></v-switch>
            </v-col>
            <v-switch hide-details  style="margin-top: 0px; margin-bottom: 10px; margin-left: 10px"
            v-model="edit_bool"
            :label="`Allow edit? ${edit_bool? 'yes': 'no'}`"
            ></v-switch>
        </v-row>
        <v-row class="fill-height" style="margin-top: 0; overflow-y: scroll">
            <v-col :cols="4" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                <v-list >
                <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                    <v-list-item dense v-for="(category) in cats" :key='category.pk' @click="selectCategory(category)">
                        
                        <b>{{category}} ({{distribution.filter(v => v.cat === category)[0].cat_count}}) </b>

                        <template v-if="edit_bool">
                            <v-btn icon color="indigo" x-small @click.stop="editcat(category)">
                                <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn icon color="indigo" x-small @click.stop="mergecat(category)">
                                <v-icon>mdi-delete</v-icon>
                            </v-btn>
                        </template>
                    </v-list-item>
                    <template v-if="edit_bool">
                        <v-list-item dense @click.stop="addcat(category)">
                            <v-icon>mdi-plus</v-icon>
                        </v-list-item>
                    </template>
                </v-list-item-group>
                </v-list>
                <!-- dialog for edit cat -->
                <v-dialog v-model="editcat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px;" >
                            <h1 style="text-align: center; padding-top: 20px; margin: 20px 5px 10px; color: blue">{{cat_toedit}}</h1>
                            <h1 style="text-align: center; margin: 20px 5px 10px"> ⬇️ </h1>
                            <v-text-field hide-details style="margin: 5px"
                                v-model="cat_new"
                                solo
                                label="Rename category"
                                clearable
                                dense
                            ></v-text-field>

                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="savecat" :disabled="disableSave">
                                save & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notsavecat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <!-- dialog for add cat -->
                <v-dialog v-model="addcat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px;" >
                            <h1 style="text-align: center; padding-top: 20px;margin: 20px 5px 10px; line-height: 1.3"> Enter the category you wish to add: </h1>
                            <v-text-field hide-details style="margin: 5px"
                                v-model="cat_toadd"
                                solo
                                label="New category here"
                                clearable
                                dense
                            ></v-text-field>

                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="savenewcat" :disabled="disableSave">
                                add & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notsavenewcat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>


                <!-- dialog for merge cat -->
                <v-dialog v-model="mergecat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px;" >
                            <h1 style="text-align: center; padding-top: 20px; margin: 20px 5px 10px; color: blue">{{cat_tomerge}}</h1>
                            <h1 style="text-align: center; margin: 20px 5px 10px"> ⬇️ </h1>
                            <v-select
                                :items="cats" label="Select category to merge" v-model="cat_mergeto" dense solo 
                            ></v-select>
                            <template v-if="cat_mergeto !== ''">
                            <h2>{{cat_tomerge}} + {{cat_mergeto}} -> <span style="color: blue">{{cat_mergeto}}</span></h2>
                            </template>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="savemergecat" :disabled="disableSave">
                                merge & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notsavemergecat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-col>

            <v-col :cols="8" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Sub-category</h4>
                <v-list>
                <v-list-item-group color="indigo"> 
                    <template v-if="distribution.filter(e => e.cat === category)[0] !== undefined">
                        <template v-if="sort_bool">
                            <v-list-item dense v-for="subcat in subcats_sorted" :key="subcat.pk" @click="seeexamples(subcat)">
                                <span class='subcat-div'>
                                    <b>{{subcat.subcat}}</b> <b>({{subcat.count}})</b>: <span style="color: gray; font-size: 85%">{{subcat.description}}</span>
                                    <template v-if="edit_bool">
                                        <v-btn icon color="indigo" x-small @click='editsubcat(subcat)'>
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        <v-btn icon color="indigo" x-small @click='editcatofsubcat(subcat)'>
                                            <v-icon>mdi-arrow-up-down</v-icon>
                                        </v-btn>
                                        <v-btn icon color="indigo" x-small @click.stop="mergesubcat(subcat)">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>
                                    </template>
                                </span>
                            </v-list-item>
                        </template>
                        <template v-if="sort_bool === false">
                            <v-list-item dense v-for="subcat in subcats" :key="subcat.pk" @click="seeexamples(subcat)" >
                                <span class='subcat-div'>
                                    <b>{{subcat.subcat}}</b> <b>({{subcat.count}})</b>: <span style="color: gray; font-size: 85%">{{subcat.description}}</span>
                                    <template v-if="edit_bool">
                                        <v-btn icon color="indigo" x-small @click='editsubcat(subcat)'>
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        <v-btn icon color="indigo" x-small @click='editcatofsubcat(subcat)'>
                                            <v-icon>mdi-arrow-up-down</v-icon>
                                        </v-btn>
                                        <v-btn icon color="indigo" x-small @click.stop="mergesubcat(subcat)">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>
                                    </template>
                                </span>
                            </v-list-item>
                        </template>
                    </template>
                </v-list-item-group>
                </v-list>

                <!-- dialog for edit subcat -->
                <v-dialog v-model="editsubcat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px; overflow-y: scroll">
                            
                            <h1 style="text-align: center; margin: 20px 5px 5px;">{{category}} - <span style="color: blue">{{subcat_toedit.subcat}}</span> <br/><span style="font-size: 70%; font-weight: normal; color: blue; margin-top: 5px">{{subcat_toedit.description}}</span></h1>
                            <h1 style="text-align: center; margin: 10px 5px"> ⬇️ </h1>
                            <v-text-field hide-details style="margin: 5px"
                                v-model="subcat_new"
                                solo
                                label="Rename sub-category"
                                clearable
                                dense
                            ></v-text-field>
                            <v-text-field hide-details style="margin: 5px"
                                v-model="desc_new"
                                solo
                                label="Rewrite description"
                                clearable
                                dense
                            ></v-text-field>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="savesubcat" :disabled="disableSave" >
                                save & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notsavesubcat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <!-- dialog for move subcat -->
                <v-dialog v-model="movecat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px; overflow-y: scroll">
                            
                            <h1 style="text-align: center; margin: 20px 5px 5px;">{{category}} - {{subcat_tomove.subcat}}</h1>
                            <h1 style="text-align: center; margin: 15px 5px"> ⬇️ </h1>
                            <v-select
                                :items="cats" label="Select category to move" v-model="cat_moveto" dense solo 
                            ></v-select>
                            <template v-if="cat_moveto !== ''">
                            <h2>Will become <span style="color: blue">{{cat_moveto}} - {{subcat_tomove.subcat}}</span></h2>
                            </template>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="movesubcat" :disabled="disableSave" >
                                move & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notmovesubcat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <!-- dialog to merge subcat -->
                <v-dialog v-model="mergesubcat_dialog" width="400" persistent>
                    <v-card>
                        <v-card-text class="text-left" style="height: 200px;" >
                            <h1 style="text-align: center; padding-top: 20px; margin: 20px 5px 10px; color: blue">{{category}} - {{subcat_tomerge}}</h1>
                            <h1 style="text-align: center; margin: 20px 5px 10px"> ⬇️ </h1>
                            <v-select
                                :items="subcats.map(v=>v.subcat)" label="Select sub-category to merge" v-model="subcat_mergeto" dense solo 
                            ></v-select>
                            <template v-if="subcat_mergeto !== ''">
                            <h2>({{category}} - {{subcat_tomerge}}) + ({{category}} - {{subcat_mergeto}}) -> <span style="color: blue">{{category}} - {{subcat_mergeto}}</span></h2>
                            </template>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="savemergesubcat" :disabled="disableSave">
                                merge & close
                            </v-btn>
                            <v-btn color="indigo lighten-2 white--text" text @click="notsavemergesubcat" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <!-- dialog for show examples -->
                <v-dialog v-model="show_example_dialog" width="800">
                    <v-card>
                        <v-card-text class="text-left" style="height: 700px; overflow-y: scroll">
                            
                            <h1 style="text-align: center; margin: 20px 5px 5px;">Examples in <span style="color:blue">{{category}} - {{subcat_clicked}}</span></h1>
                            <v-row>
                                <v-col cols="auto" v-for="(annot, idx) in examples_toshow" :key="idx" style="margin: 0 10px">
                                <v-img :src="imageNo2Url(annot.image_no)" width="300">
                                    <div v-if="annot_boxes[annot.image_no]">
                                        <div style="margin: 0; background: gray; color: white; font-size: 90%; text-align: center">
                                            {{annot_boxes[annot.image_no].map(v=>v.text)}}
                                        </div>
                                        <div v-for="box in annot_boxes[annot.image_no]" :key="box.id"><!--{{annot_boxes[annot.issue_pk].length}}-->
                                            <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                                        </div>
                                    </div>
                                    <div style="opacity: 0.0;">{{waitForJson(annot.image_no, annot.image_no, annot.boxes_id)}}</div>
                                </v-img>
                            </v-col>
                            </v-row>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo lighten-2 white--text" text @click="unseeexamples" >
                                close
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
import { mapActions } from 'vuex';
import BoundingBox from '@/components/BoundingBox.vue'

export default {
    name: "FinalDataset",
    components: {
        BoundingBox
    },
    data() {
        return {
            cats: [],
            subcats: [],
            subcats_sorted: [],
            
            //selected category
            category: 'menu',
            subcategory: '',

            sel_category: 0,

            distribution: this.$store.getters.getDistribution,

            sort_bool: false,
            edit_bool: false,

            // dialogs
            editcat_dialog: false,
            editsubcat_dialog: false,
            movecat_dialog: false,
            addcat_dialog: false,
            mergecat_dialog: false,
            mergesubcat_dialog: false,

            // sources
            cat_toedit: [],
            subcat_toedit: [],
            subcat_tomove: [],
            cat_tomerge: '',
            subcat_tomerge: '',
            
            // destinations
            cat_new: '',
            subcat_new: '',
            desc_new: '',

            cat_toadd: '',
            cat_moveto: '',
            cat_mergeto: '',
            subcat_mergeto: '',


            show_example_dialog: false,
            subcat_clicked: '',
            examples_toshow: [],

            annot_boxes: {},

        }
    },

    mounted: function() {
        const self = this;
        setTimeout(
            function() {
                self.distribution = self.$store.getters.getDistribution
                self.cats = self.distribution.map(v => v.cat)
                self.category = self.cats[0]
                if(self.distribution.filter(e => e.cat === self.category)[0]){
                    self.subcats = self.distribution.filter(e => e.cat === self.category)[0].subcat_distn
                    self.subcats_sorted = [...self.subcats].sort((a, b) => b.count - a.count)
                }
            }
        , 1000)

        self.$store.subscribeAction({after: (action) => {
            if (action.type === 'updateDistribution') {
                self.distribution = self.$store.getters.getDistribution
                self.cats = self.distribution.map(v => v.cat)
                self.category = self.cats[0]
                if(this.distribution.filter(e => e.cat === this.category)[0]){

                    self.subcats = self.distribution.filter(e => e.cat === this.category)[0].subcat_distn
                    self.subcats_sorted = [...self.subcats].sort((a, b) => b.count - a.count)
                //console.log("UPDATE DISTRIBUTION JUST CALLED", self.distribution)
                }
            }
        }})
    },

    methods: {
        ...mapActions(['updateDistribution']),
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            if(this.distribution.filter(e => e.cat === this.category)[0]){
                this.subcats = this.distribution.filter(e => e.cat === this.category)[0].subcat_distn
                this.subcats_sorted = [...this.subcats].sort((a, b) => b.count - a.count)
                //console.log(this.subcats.map(v=>v.subcat+" "+v.count), this.subcats_sorted.map(v=>v.subcat+" "+v.count))
            }
            this.addsubcat=false;
        },

        
        // Modify cat
        editcat(cat) {
            this.cat_toedit = cat
            this.editcat_dialog = true
        },


        savecat() {
            const self = this
            console.log("CAT CHANGE", self.cat_toedit, "to", self.cat_new)
            axios.post(self.$store.state.server_url + '/dashboard/change-cat-text/', {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.docType,
                old_cat: self.cat_toedit,
                new_cat: self.cat_new
            }).then(function () {
                self.editcat_dialog = false
                self.cat_toedit = ''
                self.cat_new = ''
            }).then(function() {
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType 
                    }
                })
                .then(function(res){
                    //console.log('new distribution', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
            })
            
        },

        notsavecat() {
            const self = this
            self.editcat_dialog = false
            self.cat_toedit = ''
            self.cat_new = ''
            
        },


        // Modify subcat and description
        editsubcat(subcat) {
            this.subcat_toedit = subcat
            this.editsubcat_dialog = true
        },

        savesubcat() {
            const self = this
            
            const subcat_old = self.subcat_toedit.subcat
            const desc_old = self.subcat_toedit.description

            if (self.desc_new !== '') {
                console.log("DESC CHANGE", desc_old, "to", self.desc_new)
                
                axios.post(self.$store.state.server_url + '/dashboard/change-subcat-description/', {
                    mturk_id: self.$store.state.mturk_id,
                    doctype: self.$route.params.docType,
                    cat: self.category,
                    subcat: subcat_old,
                    new_description: self.desc_new
                }).then(function () {
                    self.subcat_toedit = ''
                    self.desc_new = ''
                    self.editsubcat_dialog = false
                }).then(function() {
                    axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                        params:{
                            mturk_id: self.$store.state.mturk_id,
                            doctype: self.$route.params.docType 
                        }
                    })
                    .then(function(res){
                        //console.log('new distribution', res.data);
                        self.curr_distribution=res.data.distribution;
                        self.updateDistribution(res.data.distribution)
                    });
                })
            }


            if (self.subcat_new !== '') {
                console.log("SUBCAT CHANGE", subcat_old, "to", self.subcat_new)
                axios.post(self.$store.state.server_url + '/dashboard/change-subcat-text/', {
                    mturk_id: self.$store.state.mturk_id,
                    doctype: self.$route.params.docType,
                    cat: self.category,
                    old_subcat: subcat_old,
                    new_subcat: self.subcat_new
                }).then(function () {
                    self.subcat_toedit = ''
                    self.subcat_new = ''
                    self.editsubcat_dialog = false
                }).then(function() {
                    axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                        params:{
                            mturk_id: self.$store.state.mturk_id,
                            doctype: self.$route.params.docType 
                        }
                    })
                    .then(function(res){
                        //console.log('new distribution', res.data);
                        self.curr_distribution=res.data.distribution;
                        self.updateDistribution(res.data.distribution)
                    });
                })
            }
            
        },

        notsavesubcat() {
            const self = this;
            self.editsubcat_dialog = false
            self.subcat_toedit = ''
            self.subcat_new = ''
        },

        // Moving subcategory
        editcatofsubcat(subcat) {
            this.subcat_tomove = subcat
            this.movecat_dialog = true
        },

        movesubcat() {
            const self = this
            console.log("MOVE CAT", self.subcat_tomove, "to", self.cat_moveto)
            axios.post(self.$store.state.server_url + '/dashboard/move-subcat/', {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.docType,
                old_cat: self.category,
                new_cat: self.cat_moveto,
                subcat: self.subcat_tomove.subcat, 
            }).then(function () {
                self.movecat_dialog = false
                self.subcat_tomove = ''
                self.cat_moveto = ''
            }).then(function() {
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType 
                    }
                })
                .then(function(res){
                    //console.log('new distribution', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
            })
        },

        notmovesubcat() {
            const self = this;
            self.movecat_dialog = false
            self.subcat_tomove = ''
            self.cat_moveto = ''
        },

        seeexamples(subcat) {
            this.annot_boxes = {}
            if (this.edit_bool === false) {
                //console.log(this.category, subcat.subcat)
                const self = this
                self.show_example_dialog = true
                self.subcat_clicked = subcat.subcat
                axios.get(self.$store.state.server_url + "/dashboard/get-examples/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType,
                        cat: self.category,
                        subcat: subcat.subcat
                    }
                })
                .then(function(res){
                    //console.log('results', res.data.examples.map(v => v.image_no + "-" + v.boxes_id));
                    self.examples_toshow = res.data.examples
                    
                });
            
            }
            
        },

        unseeexamples() {
            const self = this
            self.show_example_dialog = false
        },


        // Add new cat
        addcat() {
            //this.cat_toedit = cat
            this.addcat_dialog = true
        },

        savenewcat() {
            const self = this
            console.log("CAT ADD", self.cat_toadd)
            axios.post(self.$store.state.server_url + '/dashboard/add-cat/', {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.docType,
                category: self.cat_toadd
            }).then(function () {
                self.addcat_dialog = false
                self.cat_toadd = ''
            }).then(function() {
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType 
                    }
                })
                .then(function(res){
                    //console.log('new distribution', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
            })
        },

        notsavenewcat() {
            const self = this;
            self.addcat_dialog = false
            self.cat_toadd = ''
        },

        // Merge cats
        mergecat(cat) {
            this.cat_tomerge = cat
            this.mergecat_dialog = true
        },

        savemergecat() {
            const self = this;
            console.log("MERGE CAT", self.cat_tomerge, "to", self.cat_mergeto)
            axios.post(self.$store.state.server_url + '/dashboard/merge-cats/', {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.docType,
                from_cat: self.cat_tomerge,
                to_cat: self.cat_mergeto
            }).then(function () {
                self.mergecat_dialog = false
                self.cat_tomerge = ''
                self.cat_mergeto = ''
            }).then(function() {
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType 
                    }
                })
                .then(function(res){
                    //console.log('new distribution', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
            })
        },

        notsavemergecat() {
            const self = this
            self.mergecat_dialog = false
            self.cat_tomerge = ''
            self.cat_mergeto = ''
        },


        // Merge subcats
        mergesubcat(subcat) {
            this.subcat_tomerge = subcat.subcat
            console.log(subcat.subcat)
            this.mergesubcat_dialog = true
        },

        savemergesubcat() {
            const self = this;
            console.log("MERGE SUBCAT", self.subcat_tomerge, "to", self.subcat_mergeto)
            axios.post(self.$store.state.server_url + '/dashboard/merge-subcats/', {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.docType,
                from_cat: self.category,
                from_subcat: self.subcat_tomerge,
                to_cat: self.category,
                to_subcat: self.subcat_mergeto
            }).then(function () {
                self.mergesubcat_dialog = false
                self.subcat_tomerge = ''
                self.subcat_mergeto = ''
            }).then(function() {
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                        mturk_id: self.$store.state.mturk_id,
                        doctype: self.$route.params.docType 
                    }
                })
                .then(function(res){
                    //console.log('new distribution', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
            })
        },

        notsavemergesubcat() {
            const self = this
            self.mergesubcat_dialog = false
            self.subcat_tomerge = ''
            self.subcat_mergeto = ''
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

                const width = 300;//cont_pos.right-cont_pos.left
                //const height = cont_pos.bottom-cont_pos.top

                const resbox = self.setImageBoxes([json, width, width*img_height/img_width, true]);
                //self.original_box = json;

                //console.log(resbox)
                //self.$forceUpdate();
                self.done = ''
                
                var boxes = []

                boxes = resbox.filter(v => box_id.includes(v.box_id))
                //console.log(boxes)
                //var texts = boxes.map(v => v.text)
                
                return boxes
            })
        },

        async waitForJson(pk, no, box_id) {
            //console.log(json)
            //console.log(pk, no, box_id)
            const response = await this.imageNo2Json(no, box_id)
            //console.log(response)
            if (this.annot_boxes[pk] === undefined) {
                this.$set(this.annot_boxes, pk, response)
                
            }
            return response
        },

    },

    computed: {
        disableSave() {
            //console.log(this.cat_new.length, "|", this.subcat_new.length, "|", this.desc_new, "|", this.cat_moveto.length)
            return this.cat_new === '' && this.subcat_new === '' && this.desc_new === '' && this.cat_moveto === '' && this.cat_toadd === '' && this.cat_mergeto === '' && this.subcat_mergeto === ''
        },

    }
}
</script>
