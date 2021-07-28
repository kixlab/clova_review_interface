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
            suggestions:[],
        }
    },

    mounted: function() {
        const self = this;
        axios.get(self.$store.state.server_url + "/dashboard/get-closeto-suggestions/",{
    }).then(function(res){
        console.log(res.data);
        self.suggestions=res.data.close_to_suggestions;

      })

    axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
    }).then(function(res){
      self.cats=res.data.cats;
      self.subcats=res.data.subcats;
      self.category=self.cats[0];
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
            console.log('add as new clicked')
        },

        ignore() {
            console.log('ignore clicked')
        },


    },

    computed: {
        disabled() {
            return false;
        }
    }

}
</script>

<style scoped>
h2 {
    margin: 10px 0 20px;
}
</style>