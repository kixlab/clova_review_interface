<template>
    <v-container fluid fill-height style="padding: 0">
        <v-row class="fill-height" style="height: 85vh;">
            <v-col cols="4" style="border: 1px solid red;"> 
                <h2>label set</h2>
                <v-row dense>
                    <v-col :cols="4" style="text-align:left;">
                        <h4>Category</h4>
                        <v-list >
                        <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                            <v-list-item v-for="category in cats.filter(v => v.cat !== 'n/a')" :key='category.pk' @click="selectCategory(category)">
                                <b>{{category.cat}}</b>
                            </v-list-item>
                        </v-list-item-group>
                        </v-list>
                    </v-col>

                    <v-col :cols="8" style="text-align:left;">
                        <h4>Sub-category</h4>
                        <v-list>
                        <v-list-item-group v-model="sel_subcategory" color="indigo"> 
                            <v-list-item v-for="subcat in subcats.filter(e => e.cat == category.cat && e.subcat !== 'n/a')" :key="subcat.pk" @click="selectSubcat(subcat)">
                                <span class='subcat-div'>
                                    <b>{{subcat.subcat}}</b>: <span style="color: gray">{{subcat.description}}</span>
                                </span>
                            </v-list-item>
                        </v-list-item-group>
                        </v-list>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2 style="margin-bottom: 10px;">corresponding annotations w/ images</h2>
                <h3>*<span style="color: blue;">{{sel_cat}} - {{sel_subcat}}</span>* selected</h3>
                <div style="height: 60vh; border: 1px solid black; text-align: left; overflow-y: scroll" >
                    
                    <div v-for="s in suggestions_show" :key="s.suggestion_pk">
                        <h4 class="suggestion">
                            Suggestion: <span style="color: blue;">{{s.suggestion_text}}</span> 
                            
                        </h4>
                        <div style="margin-bottom: 10px">
                            <v-btn style="margin-left: 30px;" outlined x-small @click="selectAll(s.annotations)">select all</v-btn>
                            <v-btn style="margin-left: 10px;" outlined x-small @click="unselectAll(s.annotations)">unselect all</v-btn>
                        </div>
                        
                        <div v-for="(annot, idx) in s.annotations" :key="annot.annot_pk" style="margin-left: 30px">
                            <v-checkbox
                                v-model="selectedBoxes"
                                :label="'#'+annot.image_no"
                                :value="annot"
                            ></v-checkbox>
                            #{{idx+1}} - {{annot.image_no}} & {{annot.boxes_id}} & {{annot.worker}}
                        </div>
                    </div>
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
                    <v-btn :disabled="disabled" @click="ignore()" color="error" class="mr-4 white--text" depressed small>
                        Ignore
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
                            small @click="saveLabels" :disabled="disableSave" style="margin: 5px 0 0 7px;"
                        >save as new</v-btn>
                    </template>
                    <v-spacer/>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";

export default {
    name: 'CloseToResolution',
    data() {
        return {
            cats: ['menu', 'subtotal', 'total', 'payment'],
            subcats: [],
            category: '',
            subcategory: '',

            sel_category: 0, 
            sel_subcategory: 0,

            sel_cat: '',
            sel_subcat: '',



            // Save selection list
            categories: [],
            
            // Show / hide save inputs
            clicked: '',

            // Selected data to save
            cat: '',
            subcat: '',
            selectedBoxes: [], // Not yet linked!

            suggestions_all:[],
            suggestions_show: [],
        }
    },

    mounted: function() {
        const self = this;
        axios.get(self.$store.state.server_url + "/dashboard/get-closeto-suggestions/",{
        })
        .then(function(res){
            //console.log(res.data);
            self.suggestions_all=res.data.close_to_suggestions;
        })

        axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
        })
        .then(function(res){
            self.cats=res.data.cats;
            self.subcats=res.data.subcats;
            self.category=self.cats[0];

            self.categories = res.data.cats.map(v => v.cat).filter(v => v !== 'n/a')
        })
    },

    methods: {
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;
        },

        selectSubcat(cat) {
            //console.log(cat.cat, cat.subcat, '-', cat.description)
            this.sel_cat = cat.cat
            this.sel_subcat = cat.subcat

            this.suggestions_show = this.suggestions_all.filter(v => v.suggestion_cat === this.sel_cat && v.suggestion_subcat === this.sel_subcat)
        },


        approve() {
            console.log('approve clicked')
        },

        addAsNew() {
            //console.log('add as new clicked')
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        ignore() {
            console.log('ignore clicked')
        },


        saveLabels() {
            console.log(this.cat, "-", this.subcat)

            // TODO
            // api call to save
            // use this.cat & this.subcat to indicate labels

            this.cat = ''
            this.subcat = ''
        },

        selectAll(annots) {
            var tempbox = this.selectedBoxes
            for (var a in annots) {
                tempbox.push(annots[a])
            }
        },

        unselectAll(annots) {
            var tempbox = this.selectedBoxes
            for (var a in annots) {
                tempbox.splice(tempbox.indexOf(annots[a]), 1)
            }
        },


    },

    watch: {
        selectedBoxes: {
            deep: true,
            handler() {
                console.log(this.selectedBoxes)
            }
        }
    },

    computed: {
        disabled() {
            return false;
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