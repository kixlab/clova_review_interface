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
            suggestions:[]
        }
    },
    mounted: function () {
    const self = this;

    axios.get(self.$store.state.server_url + "/dashboard/get-na-suggestions/",{
    }).then(function(res){
        self.suggestions=res.data.na_suggestions;
      })
      },

    methods: {
        
        approve() {
            console.log('approve clicked')
        },

        addAsNew() {
            console.log('add as new clicked')
        },

        addToExisting() {
            console.log('add to existing clicked')
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