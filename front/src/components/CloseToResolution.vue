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
                <h2>corresponding annotations w/ images</h2>
                <div style="height: 60vh; border: 1px solid black">
                    <h4>*{{sel_cat}} - {{sel_subcat}}* selected</h4>
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



            categories: ['Menu', 'Subtotal', 'Total', 'Payment'],
            subcategories: [], 

            clicked: '',

            // Selected data to save
            cat: '',
            subcat: '',
            selectedBoxes: [], // Not yet linked!
        }
    },

    mounted: function() {
        const self = this;
        axios.get(self.$store.state.server_url + "/api/get-cats", {
            params: {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.doctype
            }
        }).then(function(res) {
            self.cats = res.data.cats;
            self.subcats = res.data.subcats;
            self.category = self.cats[0];
        })
    },

    methods: {
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;
        },

        selectSubcat(cat) {
            console.log(cat.cat, cat.subcat, '-', cat.description)
            this.sel_cat = cat.cat
            this.sel_subcat = cat.subcat
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
</style>