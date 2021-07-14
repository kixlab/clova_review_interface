<template>
    <v-col cols="12">
        <v-card>
            <v-card-title style="padding: 8px;">
                <h4>Worker-level analysis</h4>
            </v-card-title>
            <v-card-text>
                <v-row style="min-height: 80vh; max-height: 90vh; overflow: scroll; padding: 0; margin-top: 6px;">
                    <v-col cols="2" style="border: 0.5px solid lightgray; min-height: 50vh; max-height: 50vh; overflow: scroll;">
                        <div v-for="(worker, index) in complete_worker_id" :key="index" v-on:click="loadWorker(worker)" style="margin: 0px 0px 5px; padding: 5px 0px; border: 1.5px solid blue; overflow: scroll; ">
                        <b>#{{index+1}}</b> - <b style="color: blue;">{{worker}}</b>
                        </div>
                    </v-col>
                    <v-col cols="10" style="border: 0.5px solid lightgray;">
                        <v-row>

                        </v-row>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
import axios from "axios";
//import {mapActions, mapGetters} from 'vuex';

export default {
    name: "OverallLabel",
    components: {

    },
    data() {
        return {
            worker: 'A8F6JFG0WSELT', // 지금 살펴보고자 하는 worker --> 나중에 worker정보 보여주는 view의 state로 가져가도 될듯!
            worker_list: [],
            complete_worker_list: [],
            worker_detail: {"username": null, "annotations":[], "start_time": null, "end_time": null},
            every_annotations: [],
            complete_worker_id: [ "A1DVKS3R9SLQ1H", "A2KJ983WWTEK4L", "APSN3KV49VLKX", "A3SLY0SJLJZ0J1", "A1IOMFFEKCWOIT", 
            "A1IU5OP7BBZHZ7", "A10NF5TK6IFNX6", "A1AYL5V5GI9HC1", "A16FY9L7QTDNRW", "A7V4CVENA0DYV", 
            "A8F6JFG0WSELT", "A3DU2EWFUGQCX4", "AZS1ZZRYENXVK", "A36T7N6CT9GUCG", "AORHXBTOCXFUK", 
            "A3GXSHLBND9E92", "A2EDER9628S0A", "AJY6J33X1KJNP", "A1NOINYD1FZ55T", "A28A3HF3LSEIDT", 
            "A4E1UYPDHE8D8", "A3DS5B06ZCD3E3", "A2A2VSZ2C8PC19", "A2BAQ26SMQQEUG", "A16X5FB3HAFCKN", 
            "A26399B1QZ7XJJ", "AJZBAP861F6X1", "A5LYLHG880ABE", "A31O43Y575I5C2", "ANUXUJE8QRE0C", 
            "A22AKWWFAN7VQM", "A3SKEW89V5S0DI", "A16U1L4R6WV5G2", "AQECGQAIABJ9X", "A2F0X4LN9N4O4C" ],
        };
    },

    mounted() {
        const self = this;

        axios.get(self.$store.state.server_url+'/api/get-workers',{
        params:{
            doctype: 'receipt' //self.$route.params.docType
        }
        }).then(function(res){
            self.worker_list = res.data;
            console.log('worker list', self.worker_list);
            for (var worker in res.data) {
                if (self.complete_worker_id.indexOf(res.data[worker].username) > -1) {
                    console.log(res.data)
                    self.complete_worker_list.push(res.data[worker].username)
                }
            }
            //console.log(self.complete_worker_list)
        })

        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-annotations-by-worker',{
        params:{
            mturk_id: self.worker
        }
        }).then(function(res){
            self.worker_detail =res.data;
            console.log('annotation by worker', self.worker_detail);
        })},500);

        axios.get(self.$store.state.server_url+'/api/get-every-annotations',{
        params:{
            doctype: 'receipt' //self.$route.params.docType
        }
        }).then(function(res){
            self.every_annotations= res.data;
            console.log('all annotations', res.data);
        })


    },

    methods: {
        loadWorker: (id) => {
            console.log(id)
        }
    },

    computed: {

    },

    watch: {

    },

}
</script>

<style scoped>

</style>