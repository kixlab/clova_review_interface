<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%"><b> 2. Choose a label that best describes the <span class="red-text">selected box(es)</span>.</b> </v-card-title>
      <v-card-subtitle class='text-left'>There are <b style="color:blue;">11 labels</b> in total. Please scroll down to take a look at all of them.</v-card-subtitle>
      <v-card-text> 
        <v-row>
          <v-col>
            <v-simple-table fixed-header height="250px">
                <template v-slot:default>
                <thead>
                    <tr>
                      <th style="textAlign: center; background-color: lightGrey;"></th>
                      <th style="textAlign: center; background-color: lightGrey;">#</th>
                      <th style="textAlign: center; background-color: lightGrey;">Category</th>
                      <th style="textAlign: center; background-color: lightGrey;">Label</th>
                      <th style="textAlign: center; background-color: lightGrey;">Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in labelTable" :key="item.id">
                      <td style="padding:0; width: 35px;">
                        <v-tooltip top>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn small icon color="darkgrey" @click="annotate(item)" :disabled=isDisabled v-bind="attrs" v-on="on">
                              <v-icon>text_rotation_down</v-icon>
                            </v-btn>
                          </template>
                          <span>annotate</span>
                        </v-tooltip>
                      </td>
                      <td style="background-color: #eee">{{ item.id }}</td>
                      <td>{{ item.label }}</td>
                      <td style="background-color: #eee">{{ item.sublabel }}</td>
                      <td>{{ item.description }}</td>
                        
                    </tr>
                </tbody>
                </template>
            </v-simple-table>
          </v-col>
        </v-row>
      </v-card-text>

    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'Labeling',
  data() {
    return {
      selection: [],
      labelTable: [
          { id: 1, label: 'menu', sublabel: 'name', description: 'Name of the menu'},
          { id: 2, label: 'menu', sublabel: 'unit price', description: 'Unit price of the menu'},
          { id: 3, label: 'menu', sublabel: 'count', description: 'Number of the menu consumed'},
          { id: 4, label: 'menu', sublabel: 'price', description: 'Total price of the menu'},
          { id: 5, label: 'subtotal', sublabel: 'subtotal price', description: 'Subotal price excluding tax'},
          { id: 6, label: 'subtotal', sublabel: 'tax price', description: 'Tax price'},
          { id: 7, label: 'total', sublabel: 'total price', description: 'Total price'},
          { id: 8, label: 'total', sublabel: 'cash price', description: 'Price paid by cash'},
          { id: 9, label: 'total', sublabel: 'credit card price', description: 'Price paid by credit card'},
          { id: 10, label: 'total', sublabel: 'change price', description: 'Amount of change received'},
          { id: 11, label: 'N/A', sublabel: 'N/A (Not Applicable)', description: 'None of the labels above matched with a box'}
          
      ],
      selected_boxes: this.$store.getters.getSelectedBoxes,
      image_box: this.$store.getters.getImageBoxes,
    }
  },
  mounted: function () {
      this.$store.subscribeAction((action) => {
          if (action.type === 'updateImageBoxes') {
              //console.log("BEING CALLED")
              this.image_box = this.$store.getters.getImageBoxes
          }
      })
  },

  methods: {
      ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes']),
      ...mapGetters(['getImageBoxes']),

      add() {
          this.$refs.form.validate()
          
          var id = this.labelTable.length
          this.labelTable.push({checked: false, id: id, label: this.label, description: this.description})
          
          this.label = ''
          this.description = ''

      },

      annotate(item) {
          
          console.log(this.getImageBoxes())
          console.log(this.image_box)
          const imageBox = this.getImageBoxes()//this.image_box
          var group = []

          for (var box in imageBox) {
              if (imageBox[box].selected === true) {
                  var currBox = this.image_box[box]
                  currBox.label = item.label + "." + item.sublabel
                  currBox.selected = false
                  currBox.annotated = true
                  group.push(currBox)
              }
          }

          this.updateImageBoxes(this.image_box)
          this.updateAnnotatedBoxes([{label: item.label + " - " + item.sublabel, boxes: group}, "add"])
      },
  },
  computed: {
    isDisabled() {
        return this.$store.getters.getSelectedBoxes.length === 0
    }
  },
}
</script>
<style scoped>

.instruction {
  text-align: left;
  padding-left: 20px;
}
.red-text {
  color:red;
  font-weight: bold;
}
.btn {
  margin-left: 1rem;
}

th {
  text-align: center; 
  background-color: lightGrey;
}
</style>