<template>
    <v-container fluid fill-height>
        <v-row align-content="start">

            <v-col cols="12">
                <v-row v-if="image_box && annot_boxes">
                    <v-col cols="auto" v-for="(box, idx) in image_box" :key="idx">
                        <div style="margin: 0; background: gray; color: white; font-size: 90%; text-align: center; width: 250px;">
                            Box #{{$route.params.idx*100+idx+1}} (Image #{{box.image_no}}) <br/>
                            <!--text: {{annot_boxes[box.image_no+'-'+box.box_id][0].text}}--> | {{box.cat}} - {{box.subcat}}
                        </div>
                    <v-img :src="imageNo2Url(box.image_no)" width="250">
                        <div v-for="box in annot_boxes[box.image_no+'-'+box.box_id]" :key="box.id">
                            <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                        </div>
                        <div style="opacity: 0.0;">{{waitForJson(box.image_no+'-'+box.box_id, box.image_no, [box.box_id])}}</div>
                    </v-img>
                    </v-col>
                </v-row>
                
            </v-col>
        </v-row>

    </v-container>
</template>


<script>

import axios from "axios";
import BoundingBox from '@/components/BoundingBox.vue'
//import Progress from '@/components/Progress.vue'



export default {
    name: 'SeeAnnotations',
    components: {
        //Progress
        BoundingBox,
    },

    data() {
        return {
            image_box: [],
            img_temp: this.$store.getters.get_curr_image,
            stats: new Array(820).fill(false),

            currIdx: 0,

            currURL: '',

            annot_boxes: [],
        }
    },


    mounted: function() {
        const self = this;
        var docType= self.$route.params.docType
        var type = self.$route.params.type

        if (docType === 'receipt' && type === 'baseline') {
            self.currURL = 'http://15.165.236.102:8000'
        } 
        else if (docType === 'receipt' && type === 'proposed') {
            self.currURL = 'http://3.38.105.16:8000'
        }
        else if (docType === 'event' && type === 'baseline') {
            self.currURL = 'http://3.38.100.202:8000'
        }
        else if (docType === 'event' && type === 'proposed') {
            self.currURL = 'http://52.78.121.66:8000'
        }

        axios.get(self.currURL+ "/dashboard/get-sample-result/", {

        })
        .then(function(res) {
            console.log(res.data.sample)
            var idx = self.$route.params.idx
            self.image_box = res.data.sample.slice(idx*100, idx*100+100)
            console.log(idx*100, idx*100+100)
        })
    },


    methods: {
        goTo: function(imgNo){
            //this.$store.commit('set_image_count', imgNo);
            this.image_box = this.$store.getters.getImageBoxes;
            this.currIdx = imgNo
            console.log(this.currIdx)
        },


        setImageBoxes(json) {
            //console.log("NEW JSON --------\n" , json)
            const img_w = json[0].meta === undefined ? json[0].image_size.width : (json[0].meta.image_size === undefined? json[0].meta.imageSize.width:json[0].meta.image_size.width)
            const img_h = json[0].meta === undefined ? json[0].image_size.height : (json[0].meta.image_size === undefined? json[0].meta.imageSize.height:json[0].meta.image_size.height)
            var ratio = 1
            var padding_x = 0
            var padding_y = 0
            if (img_w/json[1] >= img_h/json[2]) {
                ratio = img_w/json[1]
                padding_y = 0//(json[2]-(img_h/ratio))/2
            } else {
                ratio = img_h/json[2]
                padding_x = (json[1]-(img_w/ratio))/2
            }

            //commit('setImageRatio', ratio)
            if(json[0].valid_line==undefined){
            const validData = (json[0]['boxes']===undefined? json[0]['words']:json[0]['boxes']);
            const processedData = validData.map(function(i) {
                if(i.box_id==undefined){
                    return {
                        box_id: i.id, 
                        text:i.text, 
                        x_pos: Math.min(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0])/ratio + padding_x, 
                        y_pos: Math.min(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1])/ratio + padding_y,
                        x_len: (Math.max(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0]) - Math.min(i.boundingBox[0][0], i.boundingBox[1][0], i.boundingBox[2][0], i.boundingBox[3][0]))/ratio, 
                        y_len: (Math.max(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1])-Math.min(i.boundingBox[0][1], i.boundingBox[1][1], i.boundingBox[2][1], i.boundingBox[3][1]))/ratio,
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.boundingBox[0][0], y1: i.boundingBox[0][1], x2: i.boundingBox[1][0], y2: i.boundingBox[0][1], y3: i.boundingBox[2][1]},
                        label: ""
                    }
                }else{
                    return {
                        box_id: i.box_id,
                        text: i.text,
                        x_pos: i.x[0]/ratio+padding_x, 
                        y_pos: i.y[0]/ratio+padding_y, 
                        x_len: (i.x[1]-i.x[0])/ratio, 
                        y_len: (i.y[2]-i.y[0])/ratio,
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.x[0], y1: i.y[0], x2: i.x[1], y2: i.y[2], y3: i.y[3]},
                        label: ""}
                }
            
            })
            return processedData
            }

            else {
            const validData=json[0].valid_line.map(v => v.words).flat(1)

            //const newValidData = []
            for (var d in json[0].valid_line) {
                var word = json[0].valid_line[d].words
                var cat = json[0].valid_line[d].category
                for (var w in word) {
                    word[w]["GTlabel"] = cat
                    //newValidData.push(word[w])
                }
            }
            //console.log("VALIDDATA", validData)
            const processedData = validData.map(function(i, idx) {
                return {box_id: idx,
                        text: i.text,
                        x_pos: i.quad.x1/ratio+padding_x, 
                        y_pos: i.quad.y1/ratio+padding_y, 
                        x_len: (i.quad.x2-i.quad.x1)/ratio, 
                        y_len: (i.quad.y3-i.quad.y2)/ratio, 
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.quad.x1, y1: i.quad.y1, x2: i.quad.x2, y2: i.quad.y2, y3: i.quad.y3},
                        label: "",
                        GTlabel: i.GTlabel,
                    }
            })
            return processedData
            }
        },

        imageNo2Url(no) {
            var docType= this.$route.params.docType
            var three_digit_id = ("00" + no).slice(-3);
            return 'http://3.38.105.16:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
        },
        imageNo2Json(no, box_id) {
            const self = this;
            var docType= this.$route.params.docType
            var three_digit_id = ("00" + no).slice(-3);
            const json_url = 'http://3.38.105.16:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
            
            return axios.get(json_url).then(function(res) {
                var json = res.data;
                var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
                var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height)
                const width = 250;//cont_pos.right-cont_pos.left
                //const height = cont_pos.bottom-cont_pos.top
                const resbox = self.setImageBoxes([json, width, width*img_height/img_width, true]);
                //self.original_box = json;
                //console.log(resbox)
                //self.$forceUpdate();
                self.done = ''
                
                var boxes = []
                boxes = resbox.filter(v => box_id.includes(v.box_id))
                //var texts = boxes.map(v => v.text)
                return boxes
            })
        },
        async waitForJson(pk, no, box_id) {
            //console.log(json)
            //console.log(no, box_id)
            const response = await this.imageNo2Json(no, box_id)
            //console.log(response)
            if (this.annot_boxes[pk] === undefined) {
                this.$set(this.annot_boxes, pk, response)
                //console.log("ANNOTBOXES", Object.keys(this.annot_boxes).length)
                //console.log('ANNOTBOXES', this.annot_boxes)
            }
            return response
        },
    }
    
}
</script>