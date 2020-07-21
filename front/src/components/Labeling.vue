<template>
  <v-col cols="12">
    <v-card tile>
      
      <v-card-title> 1. Which label best describes the selected blue box(es)? </v-card-title>
      <v-card-text> 
        <v-row>
          <v-col>
            <v-treeview
              v-model="selection"
              :items="items"
              selection-type="leaf"
              selectable
              return-object
              open-on-click
              open-all
              dense
            ></v-treeview>
          </v-col>
          <v-divider vertical></v-divider>
          <v-col class="pa-6" cols="6">
            <template v-if="!selection.length">
              No nodes selected.
            </template>
            <template v-else>
              <div v-for="node in selection" :key="node.id">
                {{ node.parentname }} / 
                {{ node.name }}
              </div>
            </template>
          </v-col>
        </v-row>
        <br/>
        <v-btn @click="labelSelected" :disabled="emptySelection"> Done </v-btn>
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
      selectionType: 'leaf',
      selection: [],
      items: [
        { 
          id: 1, 
          name: 'store',
          children: [
            { id: 2, name: 'store.nm', parentname: 'store' },
            { id: 3, name: 'store.phnm', parentname: 'store'},
          ],
        },
        {
          id: 4,
          name: 'menu',
          children: [
            { id: 5, name: 'menu.nm', parentname: 'menu' },
            { id: 6, name: 'menu.price', parentname: 'menu' },
            { id: 7, name: 'menu.cnt', parentname: 'menu' }
          ],
        },
        { 
          id: 8, 
          name: 'total',
          children: [
            { id: 9, name: 'total.cnt', parentname: 'total' },
            { id: 10, name: 'total.price', parentname: 'total' },
          ],
        },
      ],
      selected_boxes: this.$store.getters.getSelectedBoxes,
      image_box: this.$store.getters.getImageBoxes,
    }
  },

  mounted: function () {
    this.image_box = this.$store.getters.getImageBoxes

    this.$store.subscribeAction((action) => {
      if (action.type === "updateImageBoxes") {
        this.image_box = this.$store.getters.getImageBoxes
      }
    }),
    this.$store.subscribe((getters) => {
      if (getters.type === "getSelectedBoxes") {
        this.selected_boxes = this.$store.getters.getSelectedBoxes
      }
    })
  },

  computed: {
    emptySelection() {
      return !(this.selection.length === 1)
    }
  },

  methods: {
    ...mapActions(['updateImageBoxes']),
    ...mapGetters(['getImageBoxes']),
    labelSelected: function() {
      this.getImageBoxes()
      const imageBox = this.image_box
      //const selectedBoxes = this.image_box.filter(v => v.selected === true)
      const label = this.selection[0].name
      
      for (var box in imageBox) {
        if (imageBox[box].selected === true) {
          console.log(this.image_box)
          this.image_box[box].label = label
          this.image_box[box].selected = false
          this.image_box[box].annotated = true
        }
      }

      //console.log(this.image_box)
      this.updateImageBoxes(this.image_box)
      this.selection = []

    }
  },
}
</script>
