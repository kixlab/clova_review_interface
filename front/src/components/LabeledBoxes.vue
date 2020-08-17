<template>
    <v-col cols="12">
        <v-card tile>
            <v-card-title># Annotation Status - hover to see corresponding boxes </v-card-title>
            <v-card-text style="min-height:200px" scrollable max-height="200px"> 
                <div v-for="group in annotated_box" :key="group.id">
                    <v-btn-toggle dense style="padding:5px">
                        <v-btn text small tile depressed class="text-none" @mouseover="highlightGroup(group.boxes)" @mouseout="undoHighlightGroup(group.boxes)"> {{group.label}} </v-btn>
                        
                        <div v-for="box in group.boxes" :key="box.id">
                            <v-btn small tile depressed @mouseover="highlight(box)" @mouseout="undoHighlight(box)" class="text-none"> 
                                {{box.text}}  
                            </v-btn>
                        </div>
                        <v-tooltip right>
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn small depressed icon @click="remove(group)" v-bind="attrs" v-on="on"> <v-icon>delete_outline</v-icon> </v-btn>
                            </template>
                            <span>remove annotation</span>
                        </v-tooltip>
                    </v-btn-toggle>
                </div>
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
    name: "LabeledBoxes",
    data() {
        return {
            image_box: this.$store.getters.getImageBoxes,
            annotated_box: this.$store.getters.getAnnotatedBoxes,
        };
    },

    mounted() {
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

        highlight(item) { item.hover = true },
        undoHighlight(item) { item.hover = false },

        highlightGroup(group) {
            for (var box in group) {
                group[box].hover = true
            }
        },

        undoHighlightGroup(group) {
            for (var box in group) {
                group[box].hover = false
            }
        },

        remove(group) {
            for (var i in this.image_box) {
                var temp = this.image_box[i]
                for (var box in group.boxes) {
                    var removedBox = group.boxes[box]
                    if (temp.x_pos === removedBox.x_pos && temp.y_pos === removedBox.y_pos) {
                        temp.annotated = false
                        temp.label = ''
                    }
                }
            }

            this.updateImageBoxes(this.image_box)
            this.updateAnnotatedBoxes([group, "remove"])
        }


    },

    
}
</script>