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
            <v-switch
            v-model="sort_bool"
            :label="`Sort with frequency: ${sort_bool? 'yes': 'no'}`"
            ></v-switch>
        </v-row>
        <v-row class="fill-height" style="margin-top: 0; overflow-y: scroll">
            <v-col :cols="4" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                <v-list >
                <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                    <v-list-item dense v-for="category in cats" :key='category.pk' @click="selectCategory(category)">
                        <b>{{category}} ({{distribution.filter(v => v.cat === category)[0].cat_count}}) </b>
                        <v-btn icon color="indigo" x-small @click='editcat'>
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </v-list-item>
                </v-list-item-group>
                </v-list>
            </v-col>

            <v-col :cols="8" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Sub-category</h4>
                <v-list>
                <v-list-item-group color="indigo"> 
                    <template v-if="distribution.filter(e => e.cat === category)[0] !== undefined">
                        <template v-if="sort_bool">
                            <v-list-item dense v-for="subcat in subcats_sorted" :key="subcat.pk" @mouseover="seeexamples(subcat)" @mouseout="unseeexamples">
                                <span class='subcat-div'>
                                    <b>{{subcat.subcat}}</b> <b>({{subcat.count}})</b>: <span style="color: gray; font-size: 85%">{{subcat.description}}</span>
                                    <v-btn icon color="indigo" x-small @click='editsubcat'>
                                        <v-icon>mdi-pencil</v-icon>
                                    </v-btn>
                                </span>
                            </v-list-item>
                        </template>
                        <template v-if="sort_bool === false">
                            <v-list-item dense v-for="subcat in subcats" :key="subcat.pk" @mouseover="seeexamples(subcat)" @mouseout="unseeexamples">
                                <span class='subcat-div'>
                                    <b>{{subcat.subcat}}</b> <b>({{subcat.count}})</b>: <span style="color: gray; font-size: 85%">{{subcat.description}}</span>
                                    <v-btn icon color="indigo" x-small @click='editsubcat'>
                                        <v-icon>mdi-pencil</v-icon>
                                    </v-btn>
                                </span>
                            </v-list-item>
                        </template>
                    </template>
                </v-list-item-group>
                </v-list>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
//import axios from "axios";
export default {
    name: "FinalDataset",
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
        }
    },
    mounted: function() {
        const self = this;
        //console.log(self);
        /*         
        axios.get(self.$store.state.server_url + "/dashboard/get-cats", {
            params: {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.doctype
            }
        }).then(function(res) {
            self.cats = res.data.cats;
            self.subcats = res.data.subcats;
            self.category = self.cats[0];
        }) 
        */
        setTimeout(
            function() {
                self.distribution = self.$store.getters.getDistribution
                self.cats = self.distribution.map(v => v.cat)
                self.category = self.cats[0]
                if(self.distribution.filter(e => e.cat === self.category)[0]){
                    self.subcats = self.distribution.filter(e => e.cat === self.category)[0].subcat_distn
                    self.subcats_sorted = [...this.subcats].sort((a, b) => b.count - a.count)
                }
            }
        , 1000)
        self.$store.subscribeAction({after: (action) => {
            if (action.type === 'updateDistribution') {
                self.distribution = self.$store.getters.getDistribution
                self.cats = self.distribution.map(v => v.cat)
                if(this.distribution.filter(e => e.cat === this.category)[0]){
                    self.subcats = self.distribution.filter(e => e.cat === this.category)[0].subcat_distn
                    self.subcats_sorted = [...this.subcats].sort((a, b) => b.count - a.count)
                //console.log("UPDATE DISTRIBUTION JUST CALLED", self.distribution)
                }
            }
        }})
    },
    methods: {
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            if(this.distribution.filter(e => e.cat === this.category)[0]){
                this.subcats = this.distribution.filter(e => e.cat === this.category)[0].subcat_distn
                this.subcats_sorted = [...this.subcats].sort((a, b) => b.count - a.count)
                //console.log(this.subcats.map(v=>v.subcat+" "+v.count), this.subcats_sorted.map(v=>v.subcat+" "+v.count))
        }
            this.addsubcat=false;
        },
        editcat() {
        },
        editsubcat() {
        },
        seeexamples(subcat) {
            console.log(this.category, subcat.subcat)
        },
        unseeexamples() {
            
        },
    }
}
</script>
