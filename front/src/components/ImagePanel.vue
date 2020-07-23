<template>
  <v-card
    tile
    width="100%"
    height="100%"
    >
    <!-- I am {{ image }}! -->
    
    <v-img :src=image_url contain width="400px" height="500px" @mousedown="clickDown" @mouseup="clickUp" style="justifyContent: center">
      <drag-select-container selectorClass="bnd" style="height: 100%; width: 100%">
        <template slot-scope="{ startPoint }">
          {{startPoint}}
        <div v-if="image_box" ref="img_box">
          <div v-for="box in image_box" :key="box.id">
            <div v-if="box.selected === true">
              <bounding-box color="stroke:blue;" :box_info="box"/>
            </div>
            <div v-else-if="box.annotated === true">
              <bounding-box color="stroke:grey;" :box_info="box"/>
            </div>
            <div v-else>
              <bounding-box color="stroke:red;" :box_info="box"/>
            </div>
          </div>
        </div>

        </template>
      </drag-select-container>
    </v-img>
    
    <v-btn @click="loadImage">Load an image from the server</v-btn>

    <h3 style="marginTop: 15px"> Annotated boxes </h3>
    <div v-for="box in image_box" :key="box.id">
      <div v-if="box.annotated === true">
        {{box.text}} - [{{box.label}}]
      </div>
    </div>
    
  </v-card>
</template>


<script>
import axios from "axios";
// import Vue from 'vue';
import {mapActions, mapGetters} from 'vuex';
import DragSelect from 'vue-drag-select/src/DragSelect.vue'
import BoundingBox from '@/components/BoundingBox.vue'

// // Bounding Box component
// const BoundingBox = Vue.component('bounding-box', {
//   props: ['color', 'x', 'y', 'w', 'h', 'border'],
//   data() {
//     return {
//       clicked: true, 
//     }
//   },
//   template: `<svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
//       <rect id="box" class="bnd" :style="color" style="fill:transparent; stroke-width:1.2;" :x="int(x)" :y="int(y)" :width="int(w)+2" :height="int(h)+2"/>
//   </svg>`,
//   methods: {
//     int: function(elem) {
//       return parseInt(elem)
//     },
//     add: function(li) {
//       var res = 0
//       for (var elem in li) {
//         res += this.int(li[elem])
//       }
//       return res
//     }
//   }
// });



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

    this.$store.subscribeAction((action) => {
      if (action.type === 'setImageBoxes') {
        //console.log("Updated")
        this.image_box = this.$store.getters.getImageBoxes
      }
    })
  },

  methods: {
    ...mapActions(['setImage', 'initializeImages', 'setImageBoxes', 'updateImageBoxes']),
    loadImage: function() {
      const self = this;
      self.setImage('00001')
      self.setImageBoxes('00001')
      .then(() => {

        axios.get("http://localhost:8000/api/image/")
          .then(function (res) {
          self.image_url = "http://localhost:8000" + res.data
        })

        .catch(function(err) {
          alert(err);
        });
      })

    },


    getInitialPosition: function() {
      const box_pos = this.$refs.img_box.getBoundingClientRect()
      console.log("Initial Position:", box_pos.x, box_pos.y)
      this.initialPosition = [box_pos.x, box_pos.y]
    },


    testClick: function(event) {
      console.log("box clicked:", event.clientX, event.clientY);
      //console.log(this.image_box)
    },

    clickDown: function(event) {
      console.log("Mousedown:", event.clientX, event.clientY);
      this.startPoint = [event.clientX, event.clientY]
    },

    clickUp: function(event) {
      console.log("Mouseup:", event.clientX, event.clientY);
      this.endPoint = [event.clientX, event.clientY]
      this.getInitialPosition()
      this.updateSelectedBoxes()
    },

    updateSelectedBoxes: function() {
      var start, end
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

      const boxes = this.image_box
      for (var box in boxes) {
        var x1 = boxes[box].x_pos
        var x2 = boxes[box].x_pos + boxes[box].x_len
        var y1 = boxes[box].y_pos
        var y2 = boxes[box].y_pos + boxes[box].y_len

        if (start[0] <= x1 && start[0] <= x2 && end[0] >= x1 && end[0] >= x2 && start[1] <= y1 && start[1] <= y2 && end[1] >= y1 && end[1] >= y2) {
          console.log("** box", box, ":", boxes[box].text, /*"(", boxes[box].x_pos, boxes[box].y_pos, ")"*/)
          if (this.image_box[box].annotated === false) {
            this.image_box[box].selected = !this.image_box[box].selected
          }
        }  
      }

      this.updateImageBoxes(this.image_box)

    },


  },
  created: function () {
    this.loadImage()
  },
  computed: mapGetters(['getImage', 'getImageBoxes', 'getImageRatio']),
  

};
</script>

<style scoped>

</style>