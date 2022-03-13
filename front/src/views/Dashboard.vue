<template>
    <v-container fluid fill-height>
        <v-row align="start">
            <v-col cols="3">
            <v-dialog
                v-model="memo"
                width="600"
            >
                <template v-slot:activator="{ on, attrs }">
                <v-btn color="indigo lighten-1" dark outlined rounded small v-bind="attrs" v-on="on" @click="getmemo" style="marginLeft: 0px; marginTop: 8px;" align="start">
                    View annotators' notes
                </v-btn>
                </template>

                <v-card>
                <v-card-title class="indigo lighten-2 white--text">
                    Annotators' Notes
                </v-card-title>
                <v-card-text class="text-left" style="height: 400px; overflow-y: scroll">
                    <div v-for="v in all_memos" :key="v.worker_id">
                        <v-card v-if="v.memo !== ''" outlined style="min-height: 50px; margin: 10px 0;"> 
                            <v-card-title>
                                Worker ID - {{v.worker_id}}
                            </v-card-title>
                            <v-card-text>
                                <div v-for="(m, idx) in v.memo.split('\n')" :key="idx">
                                    {{m}} <br>
                                </div>
                            </v-card-text>
                        </v-card>
                    </div>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="indigo lighten-2 white--text" text @click="memo=false" >
                        close
                    </v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
                </v-card>
            </v-dialog>
            <v-spacer/>
            </v-col>
            <v-col cols="7">
            <v-btn-toggle v-model="toggle_exclusive" class="py-2" color="indigo">
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase" @click="clickTab"> 
                    <span><b><b>N/A</b></b> suggestion</span>
                </v-btn>
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase" @click="clickTab">
                    <span><b><b>Close to</b></b> suggestion</span>
                </v-btn>
            </v-btn-toggle>
            
            </v-col>
        </v-row>

        <v-row style="border: 1px solid black; height: 85vh">
            <v-col cols="9" style="border: 1px solid black; padding-top: 0">
                <template v-if="toggle_exclusive === 0">
                    <na-resolution/>
                </template>
                <template v-else-if="toggle_exclusive === 1">
                    <close-to-resolution/>
                </template>
                <template v-else>
                    <h2>Please select one of the two suggestion types ☝️ to begin resolution.</h2>
                </template>
            </v-col>
            <v-col cols="3" style="border: 1px solid black;">
                <h2>Final dataset</h2>
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
            curr_distribution:[],


            // See memo
            memo:false,
            memo_content: "",
            all_memos: [{worker_id: 'dummy worker id', memo: 'dummy memo'}, {worker_id: 'dummy worker 2', memo: ''}, {worker_id: 'dummy worker 3', memo: 'dummy memo content 3'}],
        }
    },
    mounted: function(){
        const self=this;

        
        
        setTimeout(
          function(){
                axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                    params:{
                mturk_id: self.$store.state.mturk_id, doctype: self.$route.params.docType }
                })
                .then(function(res){
                    //console.log('curr', res.data);
                    self.curr_distribution=res.data.distribution;
                    self.updateDistribution(res.data.distribution)
                });
          }, 500);
        axios.get(self.$store.state.server_url + "/dashboard/get-raw-distribution/",{
             params:{
          mturk_id: self.$store.state.mturk_id, doctype: self.$route.params.docType }
        })
        .then(function(res){
            //console.log('raw', res.data);
            self.raw_distribution=res.data.distribution;
        })

        self.getmemo()

    },

    methods: {
        ...mapActions(['updateDistribution', 'updateDistribution', 'setServerURL']),

        clickTab() {
            const self = this
            axios.get(self.$store.state.server_url + "/dashboard/get-curr-distribution/",{
                params:{
            mturk_id: self.$store.state.mturk_id, doctype: self.$route.params.docType }
            })
            .then(function(res){
                //console.log('curr', res.data);
                self.curr_distribution=res.data.distribution;
                self.updateDistribution(res.data.distribution)
            });
        },

        getmemo() {
            const self = this
            axios.get(self.$store.state.server_url + "/dashboard/get-all-memo/", {
                params: {
                    doctype: self.$route.params.docType
                }
            }).then(function(res) {
                //console.log(res.data.memos)
                self.all_memos = res.data.memos
            })
        },
    }
}
</script>

<style scoped>
h2 {
    margin: 10px 0 20px;
}
</style>