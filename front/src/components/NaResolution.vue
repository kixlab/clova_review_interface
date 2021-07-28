<template>
    <v-container fluid fill-height style="padding: 0">
        <v-row class="fill-height" style="height: 100vh;">
            <v-col cols="4" style="border: 1px solid red;">
                <h2>n/a suggestions</h2>
            </v-col>
            <v-col cols="8" style="border: 1px solid red;">
                <h2>corresponding annotations w/ images</h2>
                <div style="height: 60vh; border: 1px solid black">
                    <h4>placeholder for images and boxes</h4>
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
                    <template v-if="clicked === 'addtoexisting'">
                        <v-select
                            :items="categories" label="Category" v-model="cat" dense solo style="width: 15%; margin-left: 5px"
                        ></v-select>
                        <v-select
                            :items="subcategories_show" label="Sub-category" v-model="subcat" dense solo style="width: 20%; margin-left: 5px"
                        ></v-select>
                        <v-btn
                            small @click="saveLabels" :disabled="disableSave" style="margin: 5px 0 0 7px;"
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

export default {
    name: 'NaResolution',
    data() {
        return {

            // Save selection list
            categories: [],
            subcategories_all: [], 
            subcategories_show: [],

            // Show / hide save inputs
            clicked: '',

            // Selected data to save
            cat: '',
            subcat: '',
            selectedBoxes: [], // Not yet linked!

            suggestions:[]
        }
    },

    mounted: function () {
        const self = this;

        axios.get(self.$store.state.server_url + "/dashboard/get-na-suggestions/",{
        })
        .then(function(res){
            self.suggestions=res.data.na_suggestions;
        })


        axios.get(self.$store.state.server_url + "/dashboard/get-cats",{
        })
        .then(function(res){
            self.categories = res.data.cats.map(v => v.cat).filter(v => v !== 'n/a')
            self.subcategories_all = res.data.subcats.filter( v => v.subcat !== 'n/a' && v.cat !== 'n/a')
        })
    },


    methods: {
        
        approve() {
            console.log('approve clicked')
        },

        addAsNew() {
            this.clicked = this.clicked === 'addasnew' ? '' : 'addasnew'
        },

        addToExisting() {
            this.clicked = this.clicked === 'addtoexisting' ? '' : 'addtoexisting'
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

    watch: {
        cat: {
            deep: true,
            handler(){
                this.subcategories_show = this.subcategories_all.filter(v => v.cat === this.cat).map(v => v.subcat)
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
</style>