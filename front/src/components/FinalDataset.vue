<template>
    <v-container fluid fill-height >
        <v-row>
            <v-col style="padding: 0; margin-bottom: 20px">
                <h3>{{distribution.map(v => v.subcat_distn.length).reduce((a, b) => a+b)}} labels & </h3>
                <h3>{{distribution.map(v => v.cat_count).reduce((a, b) => a+b)}} annotations in total</h3>
            </v-col>
        </v-row>
        <v-row dense class="fill-height" style="margin-top: 0;">
            <v-col :cols="4" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Category</h4>
                <v-list >
                <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                    <v-list-item v-for="category in cats" :key='category.pk' @click="selectCategory(category)">
                        <b>{{category}} ({{distribution.filter(v => v.cat === category)[0].cat_count}}) </b>
                    </v-list-item>
                </v-list-item-group>
                </v-list>
            </v-col>

            <v-col :cols="8" style="text-align:left;">
                <h4 style="background-color: #3F51B5; color: #E8EAF6">Sub-category</h4>
                <v-list>
                <v-list-item-group color="indigo"> 
                    <template v-if="distribution.filter(e => e.cat === category)[0] !== undefined">
                    <v-list-item v-for="subcat in subcats" :key="subcat.pk">
                        <span class='subcat-div'>
                            <b>{{subcat.subcat}}</b> <b>({{subcat.count}})</b>: <span style="color: gray">{{subcat.description}}</span>
                        </span>
                    </v-list-item>
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
            category: 'menu',
            subcategory: '',

            sel_category: 0,

            distribution: this.$store.getters.getDistribution,
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
        self.distribution = self.$store.getters.getDistribution
        self.cats = self.distribution.map(v => v.cat)
        self.subcats = self.distribution.filter(e => e.cat === this.category)[0].subcat_distn.sort((a, b) => b.count - a.count)


        self.$store.subscribeAction({after: (action) => {
            if (action.type === 'updateDistribution') {
                self.distribution = self.$store.getters.getDistribution
                self.cats = self.distribution.map(v => v.cat)
                self.subcats = self.distribution.filter(e => e.cat === this.category)[0].subcat_distn.sort((a, b) => b.count - a.count)
                console.log(self.distribution)
            }
        }})
    },

    methods: {
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.subcats = this.distribution.filter(e => e.cat === this.category)[0].subcat_distn.sort((a, b) => b.count - a.count)
            //console.log(this.subcats)
            this.addsubcat=false;
        },


    }
}
</script>