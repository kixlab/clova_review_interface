<template>
    <v-col cols="12">
        <v-card tile>
            <v-card-title style="font-size: 110%" class="text-left"><b>3. Hover to see corresponding boxes on the image.</b> </v-card-title>
            <v-card-text style="min-height:200px; max-height: 200px; text-align:left; overflow-y: scroll;" scrollable>
                <div v-if="isAnnotationExist">
                    No annotations yet for this image :-(
                </div>
                <div v-else>
                    <v-btn small color="secondary" depressed @click="reset" style="margin-bottom: 10px"> Undo all annotations </v-btn>
                    <div v-for="group in annotated_box" :key="group.id">
                        <v-btn-toggle dense style="padding:5px" class="flex-wrap">
                            <v-btn text small tile depressed @mouseover="highlightGroup(group.boxes)" @mouseout="undoHighlightGroup(group.boxes)" style="border: 0.1px solid #eeeeee !important;"> 
                                {{group.label}} 
                            </v-btn>
                            
                            <div v-for="box in group.boxes" :key="box.id">
                                <v-btn small tile depressed @mouseover="highlight(box)" @mouseout="undoHighlight(box)" style="padding:0 3.5px; min-width:0px; border: 0.1px solid #eaeaea !important; font-size:80%; background-color: #f1f1f1"> 
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
        this.$store.subscribeAction({after: (action) => {
            if (action.type === 'updateImageBoxes') {
                //console.log("BEING CALLED")
                this.image_box = this.$store.getters.getImageBoxes
            }
            if (action.type === 'updateAnnotatedBoxes') {
                this.annotated_box = this.$store.getters.getAnnotatedBoxes
            }
            
        }})

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
        },

        reset() {
            for (var i in this.image_box) {
                var temp = this.image_box[i]
                    temp.annotated = false
                    temp.label = ''
            }

            this.updateImageBoxes(this.image_box)
            this.updateAnnotatedBoxes([[], "reset"])
        }


    },
    computed: {
        isAnnotationExist () {
            return (this.annotated_box.length < 1)
        }
    }

    
}
</script>
