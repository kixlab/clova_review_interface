<template>
    <v-container fluid fill-height>
        <v-row justify="center">
            <v-btn-toggle v-model="toggle_exclusive" class="py-2" color="indigo">
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase">
                    <span><b><b>N/A</b></b> resolution</span>
                </v-btn>
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase">
                    <span><b><b>Close to</b></b> resolution</span>
                </v-btn>
            </v-btn-toggle>
        </v-row>

        <v-row style="border: 1px solid black; height: 85vh">
            <v-col cols="9" style="border: 1px solid black;">
                <template v-if="toggle_exclusive === 0">
                    <na-resolution/>
                </template>
                <template v-else-if="toggle_exclusive === 1">
                    <close-to-resolution/>
                </template>
                <template v-else>
                    <h2>Please select one of the two resolution buttons ☝️ to begin.</h2>
                </template>
            </v-col>
            <v-col cols="3" style="border: 1px solid black;">
                <h2>Final label set & annotation</h2>
                <final-dataset/>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import NaResolution from '@/components/NaResolution.vue'
import CloseToResolution from '@/components/CloseToResolution.vue'
import FinalDataset from '@/components/FinalDataset.vue'
import axios from "axios";
import {mapActions} from 'vuex';

export default {
    name: "Dashboard",
    components: {
        NaResolution,
        CloseToResolution,
        FinalDataset,
    },

    data() {
        return {
            toggle_exclusive: null,
            raw_distribution:[],
            curr_distribution:[]
        }
    },
    mounted: function(){
        const self=this;

        setTimeout(
          function(){
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                mturk_id: self.$store.state.mturk_id }
                })
                .then(function(res){
                    console.log('curr', res.data);
                    self.curr_distribution=res.data.distribution;

                    self.updateDistribution(res.data.distribution)
                });
          },1000);
        axios.get(self.$store.state.server_url + "/dashboard/get-raw-distribution/",{
             params:{
          mturk_id: self.$store.state.mturk_id }
        })
        .then(function(res){
            console.log('raw', res.data);
            self.raw_distribution=res.data.distribution;
        })

    },

    methods: {
        ...mapActions(['updateDistribution'])
    }
}
</script>

<style scoped>
h2 {
    margin: 10px 0 20px;
}
</style>