<template>
    <v-container fluid fill-height >
        <v-row dense class="fill-height" style="margin-top: 0;">
            <v-col :cols="4" style="text-align:left;">
                <h4>Category</h4>
                <v-list >
                <v-list-item-group v-model="sel_category" active-class="border" color="indigo">
                    <v-list-item v-for="category in cats.filter(v => v.cat !== 'n/a')" :key='category.pk' @click="selectCategory(category)">
                        <b>{{category.cat}} (140) </b>
                    </v-list-item>
                </v-list-item-group>
                </v-list>
            </v-col>

            <v-col :cols="8" style="text-align:left;">
                <h4>Sub-category</h4>
                <v-list>
                <v-list-item-group color="indigo"> 
                    <v-list-item v-for="subcat in subcats.filter(e => e.cat == category.cat && e.subcat !== 'n/a')" :key="subcat.pk">
                        <span class='subcat-div'>
                            <b>{{subcat.subcat}}</b>: <span style="color: gray">{{subcat.description}}</span> <b>(43)</b>
                        </span>
                    </v-list-item>
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
            cats: ['menu', 'subtotal', 'total', 'payment'],
            subcats: [],
            category: '',
            subcategory: '',

            sel_category: null,
        }
    },

    mounted: function() {
        const self = this;
        console.log(self);
/*         axios.get(self.$store.state.server_url + "/dashboard/get-cats", {
            params: {
                mturk_id: self.$store.state.mturk_id,
                doctype: self.$route.params.doctype
            }
        }).then(function(res) {
            self.cats = res.data.cats;
            self.subcats = res.data.subcats;
            self.category = self.cats[0];
        }) */
    },

    methods: {
        selectCategory(selectedCategory){
            this.category=selectedCategory;
            this.addsubcat=false;
        },
    }
}
</script>