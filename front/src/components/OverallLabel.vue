<template>
    <v-col cols="12">
        <v-card>
            <v-card-title>
                <h2>Worker-level analysis</h2> 
                <h3 style="margin-left: 30px; margin-top: 3px;">{{worker}} - images #{{worker_detail.start_image_no}} to #{{worker_detail.end_image_no}} - total {{total_annotation_no}} annotations</h3>
            </v-card-title>
            <v-card-text>
                <v-row dense style="min-height: 80vh; max-height: 80vh; margin-top: 6px;">
                    <v-col cols="2" style="border: 0.5px solid lightgray; min-height: 50vh; max-height: 50vh; overflow: scroll;">
                        <div v-for="(workerId, index) in complete_worker_id" :key="index" v-on:click="loadWorker(workerId)" style="margin: 0px 0px 5px; padding: 5px 0px; border: 1.5px solid gray; overflow: scroll;">
                            <div v-if="workerId === worker">
                                <b>#{{index+1}}</b> - <b style="color: red;">{{workerId}}</b>
                            </div>
                            <div v-else>
                                <b>#{{index+1}}</b> - <b style="color: blue;">{{workerId}}</b>
                            </div>
                        </div>
                    </v-col>
                    <v-col cols="10" style="border: 0px solid lightgray;">
                        <v-row style="padding: 13px">
                            <v-col cols="4">
                                <h2>Accuracy compared with GT</h2>
                                <h3 style="margin-top: 15px">Overall accuracy: {{add_all(correct_labels)}} out of {{total_annotation_no}} <b style="color:blue">({{(add_all(correct_labels)/add_all(worker_annotation.map(v => v.annotations.length))*100).toFixed(2)}}%)</b></h3>
                                <div style="overflow: scroll; max-height: 70vh; margin-top: 10px">
                                    <div v-for="(img, index) in worker_annotation" :key="index" class="datarow" >
                                        <div v-if="(correct_labels[index]/img.annotations.length*100) >= 90">
                                            #{{worker_detail.user_order*7+index}}: {{img.annotations.filter(v => v.correct).length}} out of {{img.annotations.length}} <b style="color:purple">({{(correct_labels[index]/img.annotations.length*100).toFixed(2)}}%)</b>
                                        </div>
                                        <div v-else>
                                            #{{worker_detail.user_order*7+index}}: {{img.annotations.filter(v => v.correct).length}} out of {{img.annotations.length}} <b>({{(correct_labels[index]/img.annotations.length*100).toFixed(2)}}%)</b>
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="4">
                                <h2>Confidence of the labels</h2>
                                <h3 style="margin-top: 15px">
                                    Exactly: {{add_all(exactly_labels)}} <b style="color:blue">({{(add_all(exactly_labels)/total_annotation_no*100).toFixed(2)}}%)</b>
                                    / Can be: {{total_annotation_no-add_all(exactly_labels)}}
                                </h3>
                                <div style="overflow: scroll; max-height: 70vh; margin-top: 10px">
                                    <div v-for="(img, index) in worker_annotation" :key="index" class="datarow" >
                                        <div v-if="(exactly_labels[index]/img.annotations.length*100) >= 90">
                                            #{{worker_detail.user_order*7+index}}: {{img.annotations.filter(v => v.confidence).length}} out of {{img.annotations.length}} <b style="color:purple">({{(exactly_labels[index]/img.annotations.length*100).toFixed(2)}}%)</b>
                                        </div>
                                        <div v-else>
                                            #{{worker_detail.user_order*7+index}}: {{img.annotations.filter(v => v.confidence).length}} out of {{img.annotations.length}} <b>({{(exactly_labels[index]/img.annotations.length*100).toFixed(2)}}%)</b>
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="4">
                                <h2>Distribution of the labels</h2>
                                <h3 style="margin-top: 15px">
                                    Top 5 labels: {{label_distribution.filter(v => v.count >= 10).map(v => v.label).sort((a, b) => b.count - a.count).slice(0, 5)}}
                                </h3>
                                <div style="overflow: scroll; max-height: 70vh; margin-top: 10px">
                                    {{add_all(label_distribution.map(v => v.count))}}
                                    <div v-for="(label, index) in label_distribution" :key="label.no" class="datarow">
                                        #{{label.no}}: {{label.label}} - {{label.count}} ({{gt_distribution[index].count}})
                                    </div>
                                    
                                </div>
                            </v-col>
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
            worker: 'Worker not yet selected', // 지금 살펴보고자 하는 worker --> 나중에 worker정보 보여주는 view의 state로 가져가도 될듯!
            worker_list: [],
            complete_worker_list: [],
            worker_detail: {"username": null, "annotations":[], "start_time": null, "end_time": null, "user_order": null},
            worker_annotation: [],
            gt_label: [],
            gt_distribution: [{'no': 0, 'label': 'menu-id', 'count': 0}, {'no': 1, 'label': 'menu-name', 'count': 0}, {'no': 2, 'label': 'menu-count', 'count': 0}, {'no': 3, 'label': 'menu-unitprice', 'count': 0}, {'no': 4, 'label': 'menu-price', 'count': 0}, {'no': 5, 'label': 'menu-n/a', 'count': 0},
            {'no': 6, 'label': 'subtotal-price', 'count': 0}, {'no': 7, 'label': 'subtotal-menu count', 'count': 0}, {'no': 8, 'label': 'subtotal-item count', 'count': 0}, {'no': 9, 'label': 'subtotal-service charge', 'count': 0}, {'no': 10, 'label': 'subtotal-tax price', 'count': 0}, {'no': 11, 'label': 'subtotal-n/a', 'count': 0},
            {'no': 12, 'label': 'total-price', 'count': 0}, {'no': 13, 'label': 'total-n/a', 'count': 0},
            {'no': 14, 'label': 'payment-cash', 'count': 0}, {'no': 15, 'label': 'payment-change', 'count': 0}, {'no': 16, 'label': 'payment-credit card', 'count': 0}, {'no': 17, 'label': 'payment-n/a', 'count': 0},
            {'no': 18, 'label': 'n/a-n/a', 'count': 0},],
            has_gt_dist: false,
            
            correct_labels: [],
            exactly_labels: [],
            total_annotation_no: 0,
            label_distribution: [{'no': 0, 'label': 'menu-id', 'count': 0}, {'no': 1, 'label': 'menu-name', 'count': 0}, {'no': 2, 'label': 'menu-count', 'count': 0}, {'no': 3, 'label': 'menu-unitprice', 'count': 0}, {'no': 4, 'label': 'menu-price', 'count': 0}, {'no': 5, 'label': 'menu-n/a', 'count': 0},
            {'no': 6, 'label': 'subtotal-price', 'count': 0}, {'no': 7, 'label': 'subtotal-menu count', 'count': 0}, {'no': 8, 'label': 'subtotal-item count', 'count': 0}, {'no': 9, 'label': 'subtotal-service charge', 'count': 0}, {'no': 10, 'label': 'subtotal-tax price', 'count': 0}, {'no': 11, 'label': 'subtotal-n/a', 'count': 0},
            {'no': 12, 'label': 'total-price', 'count': 0}, {'no': 13, 'label': 'total-n/a', 'count': 0},
            {'no': 14, 'label': 'payment-cash', 'count': 0}, {'no': 15, 'label': 'payment-change', 'count': 0}, {'no': 16, 'label': 'payment-credit card', 'count': 0}, {'no': 17, 'label': 'payment-n/a', 'count': 0},
            {'no': 18, 'label': 'n/a-n/a', 'count': 0},],

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
            //console.log('worker list', self.worker_list);
            for (var worker in res.data) {
                if (self.complete_worker_id.indexOf(res.data[worker].username) > -1) {
                    self.complete_worker_list.push(res.data[worker].username)
                }
            }
            //console.log(self.complete_worker_list)
        })

        self.has_gt_dist = false;

        /*
        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-annotations-by-worker',{
        params:{
            mturk_id: self.worker
        }
        }).then(function(res){
            self.worker_detail =res.data;
            console.log('annotation by worker', self.worker_detail);
        })},500);
        */

        /* VERY SLOW
        axios.get(self.$store.state.server_url+'/api/get-every-annotations',{
        params:{
            doctype: 'receipt' //self.$route.params.docType
        }
        }).then(function(res){
            self.every_annotations= res.data;
            console.log('all annotations', res.data);
        })
        */


    },

    methods: {
        loadWorker(workerId) {
            const self = this;
            self.worker = workerId
            axios.get(self.$store.state.server_url+'/api/get-annotations-by-worker',{
            params:{
                mturk_id: workerId
            }
            }).then(function(res){
                self.worker_detail = res.data;
                console.log('annotation by worker', self.worker_detail);
                self.worker_annotation = res.data.annotations

                self.loadGT(res.data)
            })
        },

        async loadGT(workerInfo) {
            const self = this;
            self.gt_label = []
            //console.log(workerInfo.start_image_no, "to", workerInfo.end_image_no)
            var image_no = Array.from({length: 21}, (_, i) => i + workerInfo.start_image_no)
            // 이미지당 돌리기 
            for (var i in image_no) {
                self.worker_annotation[i]["image_no"] = image_no[i]

                // GT Json 가져오기
                var three_digit_id = ("00" + image_no[i]).slice(-3);
                const server_url = 'http://13.125.191.49:8000'
                const docType = "receipt"
                var json_url = server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
                await fetch(json_url)
                .then(response => response.json())
                .then(json => {
                    const validData=json.valid_line.map(v => v.words).flat(1)

                    for (var d in json.valid_line) {
                        var word = json.valid_line[d].words
                        var cat = json.valid_line[d].category
                        for (var w in word) {
                            word[w]["GTlabel"] = cat
                        }
                    }
                    var processedData = validData.map(function(i, idx) {
                        return {box_id: idx,
                                text: i.text,
                                GTlabel: i.GTlabel,
                            }
                    })
                    self.gt_label.push({"image_no": image_no[i], "annotations": processedData})
                });
                
            }
            
        },

        gt_to_cat(label) {
            var newlabel = label
            //newlabel = label.split(".")
            newlabel = newlabel === 'menu.num' ? 'menu.id' : newlabel
            newlabel = newlabel === 'menu.nm' ? 'menu.name' : newlabel
            newlabel = newlabel === 'menu.cnt' ? 'menu.count' : newlabel
            newlabel = (['menu.discountprice', 'menu.itemsubtotal', 'menu.vatyn', 'menu.etc', 
            'menu.sub_nm', 'menu.sub_unitprice', 'menu.sub_cnt', 'menu.sub_price', 'menu.sub_etc'].indexOf(newlabel) > -1) ? 'menu.n/a' : newlabel

            newlabel = newlabel === 'sub_total.subtotal_price' ? 'subtotal.price' : newlabel
            newlabel = newlabel === 'total.menutype_cnt' ? 'subtotal.menu count' : newlabel
            newlabel = newlabel === 'total.menuqty_cnt' ? 'subtotal.item count' : newlabel
            newlabel = newlabel === 'sub_total.service_price' ? 'subtotal.service charge' : newlabel
            newlabel = newlabel === 'sub_total.tax_price' ? 'subtotal.tax price' : newlabel
            newlabel = (['sub_total.discount_price', 'sub_total.othersvc_price', 'sub_total.etc'].indexOf(newlabel) > -1) ? 'sub_total.n/a': newlabel

            newlabel = newlabel === 'total.total_price' ? 'total.price' : newlabel
            newlabel = newlabel === 'total.total_etc' ? 'total.n/a' : newlabel

            newlabel = newlabel === 'total.cashprice' ? 'payment.cash' : newlabel
            newlabel = newlabel === 'total.changeprice' ? 'payment.change' : newlabel
            newlabel = newlabel === 'total.creditcardprice' ? 'payment.credit card' : newlabel
            newlabel = newlabel === 'total.emoneyprice' ? 'payment.n/a' : newlabel

            newlabel = newlabel.split(".")

            newlabel[0] = newlabel[0] === 'sub_total' ? 'subtotal' : newlabel[0]
            return {cat: newlabel[0], subcat: newlabel[1]}
        },

        add_all(list) {
            return list.reduce((a, b) => a + b, 0)
        }
    },

    computed: {

    },

    watch: {
        gt_label: {
            deep: true,
            handler() {
                const self = this;
                if (self.gt_label.length === 21) {
                    var image_no = Array.from({length: 21}, (_, i) => i + self.worker_detail.start_image_no)
                    self.correct_labels = []
                    self.exactly_labels = []
                    for (var l in self.label_distribution) {
                        self.label_distribution[l].count = 0
                    }
                    for (var i in image_no) {
                        
                        for (var j in self.worker_annotation[i].annotations) {
                            var temp_annotation = self.worker_annotation[i].annotations[j]
                            temp_annotation['correct'] = false

                            temp_annotation["gt_cat"] = self.gt_to_cat(self.gt_label[i].annotations[j].GTlabel).cat
                            temp_annotation["gt_subcat"] = self.gt_to_cat(self.gt_label[i].annotations[j].GTlabel).subcat
                            
                            if (temp_annotation.cat === temp_annotation.gt_cat && temp_annotation.subcat === temp_annotation.gt_subcat) {
                                temp_annotation['correct'] = true
                            }
                            var find = self.label_distribution.filter(v => v.label === temp_annotation.cat+"-"+temp_annotation.subcat)
                            find[0].count += 1

                            if (!self.has_gt_dist) {
                                var find2 = self.gt_distribution.filter(v => v.label === temp_annotation.gt_cat+"-"+temp_annotation.gt_subcat)
                                find2[0].count += 1
                            }
                            
                        }
                        //console.log(self.worker_annotation[i].annotations)
                        self.correct_labels.push(self.worker_annotation[i].annotations.filter(v => v.correct).length)
                        self.exactly_labels.push(self.worker_annotation[i].annotations.filter(v => v.confidence).length)
                    }
                    console.log("Update done!")
                    self.has_gt_dist = true
                    self.total_annotation_no = this.add_all(self.worker_annotation.map(v => v.annotations.length))
                }
                
                    
                    
            }
        }
    },

}
</script>

<style scoped>

.datarow{
    height: 30px !important;
    margin: auto;
    line-height: 30px !important;
    /*border-bottom: 1px solid !important;*/
}
</style>