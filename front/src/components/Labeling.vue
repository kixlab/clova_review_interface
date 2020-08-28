<template>
  <v-col cols="12">
    <v-card tile>
      <h3 class="instruction"> <br> 2. Choose a label that best describes the <span class="blue-text">selected box(es)</span>. </h3>
      <v-card-text> 
        <v-row>
          <v-col>
            <v-simple-table fixed-header height="250px">
                <template v-slot:default>
                <thead>
                    <tr>
                        <th style="textAlign: center"></th>
                        <th style="textAlign: center">Label</th>
                        <th style="textAlign: center">Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in labelTable" :key="item.id">
                        <td style="padding:0">
                            <v-tooltip top>
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn small icon color="darkgrey" @click="annotate(item)" :disabled=isDisabled v-bind="attrs" v-on="on">
                                        <v-icon>edit</v-icon>
                                    </v-btn>
                                </template>
                                <span>annotate</span>
                            </v-tooltip>
                        </td>
                        <td>{{ item.label }}</td>
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
          { id: 1, label: 'menu.name', description: 'Name of the menu'},
          { id: 2, label: 'menu.unit_price', description: 'Unit price of the menu'},
          { id: 3, label: 'menu.count', description: 'Number of the menu consumed'},
          { id: 4, label: 'menu.price', description: 'Total price of the menu'},
          { id: 5, label: 'subtotal.subtotal_price', description: 'Subotal price excluding tax'},
          { id: 6, label: 'subtotal.tax_price', description: 'Tax price'},
          { id: 7, label: 'total.total_price', description: 'Total price'},
          { id: 8, label: 'total.cash_price', description: 'Price paid by cash'},
          { id: 9, label: 'total.credit_card_price', description: 'Price paid by credit card'},
          { id: 10, label: 'total.change_price', description: 'Amount of change received'},
          { id: 11, label: 'N/A (Not Applicable)', description: 'None of the labels above matched with a box'}
          
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
                  currBox.label = item.label
                  currBox.selected = false
                  currBox.annotated = true
                  group.push(currBox)
              }
          }

          this.updateImageBoxes(this.image_box)
          this.updateAnnotatedBoxes([{label: item.label, boxes: group}, "add"])
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
.blue-text {
  color:blue;
  font-weight: bold;
}
.btn {
  margin-left: 1rem;
}
</style>