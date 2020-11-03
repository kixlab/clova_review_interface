<template>
 <v-col cols="12">
  <v-card
    tile
    width="100%"
    @mousedown="clickDown" @mouseup="clickUp"
    >
    <v-card-title style="font-size: 110%"><b> 1. Drag or click to select <span class="red-text">red box(es)</span> on the image. </b></v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="6">
          <v-img :src=image_url contain width="450" height="560" style="justifyContent: center">
            <drag-select-container selectorClass="bnd" style="height: 100%; width: 100%">
              <template slot-scope="{ startPoint }">
                {{startPoint}}
              <div v-if="image_box" ref="img_box">
                <div v-for="box in image_box" :key="box.id">
                  <div v-if="box.selected === true">
                    <bounding-box circle="no" color="stroke:red; stroke-width:2px; fill:red; fill-opacity:0.1;" :box_info="box"/>
                  </div>
                  <div v-else-if="box.annotated === true && box.hover === false">
                    <bounding-box circle="no" color="stroke:grey; fill:grey; fill-opacity:0.4;" :box_info="box"/>
                  </div>
                  <div v-else-if="box.annotated === true && box.hover === true">
                    <bounding-box circle="no" color="stroke:yellow; fill: rgb(220, 223, 131); fill-opacity: 0.4;" :box_info="box"/>
                  </div>
                  <div v-else>
                    <bounding-box circle="yes" color="stroke:rgb(255, 105, 105); stroke-dasharray:0;" :box_info="box"/>
                  </div>
                </div>
              </div>

              </template>
            </drag-select-container>
          </v-img>
        </v-col>

        <v-col cols="6">
          <div class="text-left" style="font-size: 100%; padding: 5px;"> 
            <b><span style="color: red">{{this.$store.getters.getImageBoxes.filter(v=>v.annotated === false).length}}</span> out of <span style="color:blue">{{this.image_box.length}}</span> boxes </b>are not yet annotated!
            <br/>
            
            <b>Selected boxes: </b>
            <div style="display:flex;" class="flex-wrap"> 
              <div v-for="elem in this.$store.getters.getImageBoxes.filter(v=>v.selected)" :key="elem.id" >
                <span style="border: 1.5px solid red; margin: 0 2px; font-size: 95%"> <b>{{ elem.text }}</b> </span>
              </div>
            </div>
            <br/>
            <v-btn small color="secondary" depressed :disabled=isDisabled @click="unselect">Undo all selections</v-btn> <span> </span>

          </div>
        </v-col>

      </v-row>

    </v-card-text>   
  </v-card>
 </v-col>
</template>


<script>
import axios from "axios";
import {mapActions, mapGetters} from 'vuex';
import DragSelect from 'vue-drag-select/src/DragSelect.vue'
import BoundingBox from '@/components/BoundingBox.vue'
import json from '../assets/receipt_00008.json';

export default {
  name: "ImagePanel",
  components: {
    BoundingBox,
    'drag-select-container': DragSelect
  },
  data() {
    return {
      image_url: {},
      image: this.$store.getters.getImage,
      image_box: this.$store.getters.getImageBoxes,
      color: 'stroke:red',
      initialPosition: [],
      startPoint: [],
      endPoint: []
    };
  },

  mounted() {
    this.image = this.$store.getters.getImage,
    this.image_box = this.$store.getters.getImageBoxes,
    this.getInitialPosition()
    if (!this.$localmode) {
      this.loadImage()
    }

    if (this.$localmode) {
      this.image_url = require('@/assets/receipt_00008.png')
      this.setImageBoxes(json)
    }

    this.$store.subscribeAction({after: (action) => {
      if (action.type === 'setImageBoxes' || action.type === 'updateAnnotatedBoxes' || action.type === 'updateImageBoxes') {
        this.image_box = this.$store.getters.getImageBoxes
      }
    }})
  },

  methods: {
    ...mapActions(/*'images', */['setImage', 'initializeImages', 'setImageBoxes', 'updateImageBoxes',]),
    //...mapActions('workers', ['initalizeImages']),
    loadImage: function() {
      const self = this;
      self.setImage('00001')
      .then(() => {
        axios.get(this.$store.state.server_url + "/api/image/")
          .then(function (res) {
          console.log(res)
          
          self.image_url = this.$store.state.server_url + res.data
        })
        .catch(function(err) {
          alert(err);
        });
      })
      .then(() => {
        axios.get(this.$store.state.server_url + "/api/image/box_info/")
          .then(function (res) {
            //console.log(res)
            self.setImageBoxes(res.data)
          //self.image_url = "http://localhost:8000" + res.data
        })
        .catch(function(err) {
          alert(err);
        });
      })
      
    },


    getInitialPosition: function() {
      const box_pos = this.$refs.img_box.getBoundingClientRect()
      //console.log("Initial Position:", box_pos.x, box_pos.y)
      this.initialPosition = [box_pos.x, box_pos.y]
    },


    testClick: function() {
      //console.log("box clicked:", event.clientX, event.clientY);
      //console.log(this.image_box)
    },

    clickDown: function(event) {
      //console.log("Mousedown:", event.clientX, event.clientY);
      this.startPoint = [event.clientX, event.clientY]
    },

    clickUp: function(event) {
      //console.log("Mouseup:", event.clientX, event.clientY);
      this.endPoint = [event.clientX, event.clientY]
      this.getInitialPosition()
      this.updateSelectedBoxes()
    },

    updateSelectedBoxes: function() {
      var start, end
      var boxes = this.image_box
      if (this.startPoint[0] === this.endPoint[0] && this.startPoint[1] === this.endPoint[1]) {
        for (var i in boxes) {
          var x11 = boxes[i].x_pos
          var x22 = boxes[i].x_pos + boxes[i].x_len
          var y11 = boxes[i].y_pos
          var y22 = boxes[i].y_pos + boxes[i].y_len
          if (x11-1 < this.startPoint[0]-this.initialPosition[0] && x22+1 > this.startPoint[0]-this.initialPosition[0] && y11-1 < this.startPoint[1]-this.initialPosition[1] && y22+1 > this.startPoint[1]-this.initialPosition[1]) {
            if (boxes[i].annotated === false) {
              boxes[i].selected = !boxes[i].selected
            }
            this.updateImageBoxes(boxes)
          }
        }
      }
      if (this.startPoint[0] <= this.endPoint[0]) {
        if (this.startPoint[1] <= this.endPoint[1]) {
          start = [this.startPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]]
          end = [this.endPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]]
        }
        else {
          start = [this.startPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]]
          end = [this.endPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]]
        }
      } 
      else {
        if (this.startPoint[1] <= this.endPoint[1]) {
          start = [this.endPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]]
          end = [this.startPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]]
        }
        else {
          start = [this.endPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]]
          end = [this.startPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]]
        }
      }

      for (var box in boxes) {
        var x1 = boxes[box].x_pos
        var x2 = boxes[box].x_pos + boxes[box].x_len
        var y1 = boxes[box].y_pos
        var y2 = boxes[box].y_pos + boxes[box].y_len

        if (start[0] <= x1 && start[0] <= x2 && end[0] >= x1 && end[0] >= x2 && start[1] <= y1 && start[1] <= y2 && end[1] >= y1 && end[1] >= y2) {
          //console.log("** box", box, ":", boxes[box].text, /*"(", boxes[box].x_pos, boxes[box].y_pos, ")"*/)
          if (this.image_box[box].annotated === false) {
            this.image_box[box].selected = !this.image_box[box].selected
          }
        }  
      }

      this.updateImageBoxes(this.image_box)

    },

    unselect: function() {
      var boxes = this.image_box
      for (var i in boxes) {
        if (boxes[i].selected === true) {
          boxes[i].selected = false
        }
      }
      this.updateImageBoxes(boxes)

    },



  },
  created: function () {
    //this.loadImage()
  },
  computed: {
    ...mapGetters(['getImage', 'getImageBoxes', 'getImageRatio']),
    isDisabled() {
      return this.$store.getters.getImageBoxes.filter(v=>v.selected).length === 0
    }
  }
  

};
</script>

<style scoped>
.instruction {
  text-align: left;
  padding-left: 20px;
  color: black;
}

.red-text {
  color: red;
  font-weight: bold;
}
</style>