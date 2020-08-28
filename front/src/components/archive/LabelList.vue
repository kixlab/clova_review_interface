<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title> # Label Panel - use or add new label-description set</v-card-title>
      <v-card-text> 
        <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
                <v-col cols="12" md="4" >
                    <v-text-field
                        v-model="label"
                        :rules="labelRules"
                        label="Label"
                        required
                        solo
                        dense
                    ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                    <v-textarea
                        v-model="description"
                        :rules="descriptionRules"
                        label="Description"
                        required
                        solo
                        dense
                        rows=1
                    ></v-textarea>
                </v-col>
                
            
                <v-col cols="12" md="2">
                    <v-btn small class="mr-4" :disabled="!valid" @click="add">add</v-btn>
                </v-col>
            </v-row>
        </v-form>
        
        <v-row>
            <v-col>
                <v-simple-table fixed-header height="250px">
                    <template v-slot:default>
                    <thead>
                        <tr>
                            <!--<th style="textAlign: center"></th>-->
                            <th style="textAlign: center">Label</th>
                            <th style="textAlign: center">Description</th>
                            <th style="textAlign: center"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in labelTable" :key="item.id">
                            <td>{{ item.label }}</td>
                            <td>{{ item.description }}</td>
                            <td width="60px" style="padding:0">
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn small icon color="darkgrey" @click="deleterow(item.id)" v-bind="attrs" v-on="on">
                                            <v-icon>remove_circle_outline</v-icon>
                                        </v-btn>
                                    </template>
                                    <span>remove label</span>
                                </v-tooltip>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn small icon color="darkgrey" @click="annotate(item)" :disabled=isDisabled v-bind="attrs" v-on="on">
                                            <v-icon>text_rotation_down</v-icon>
                                        </v-btn>
                                    </template>
                                    <span>annotate</span>
                                </v-tooltip>
                            </td>
                        </tr>
                    </tbody>
                    </template>
                </v-simple-table>
            </v-col>
        </v-row>
        <!--
        <v-row>
            <v-col>
                <v-btn @click="annotate"> annotate </v-btn>
            </v-col>
        </v-row>
        -->
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'


export default {
    name: 'LabelingScratch',
    data() {
        return {
            valid: false,
            label: '',
            description: '',
            labelRules: [
                v => !!v || 'No empty label'
            ],
            descriptionRules: [
                v => !!v || 'No empty description',
                v => v.length >= 10 || 'Description must be more than 10 characters',
            ],

            labelTable: [
                { id: 1, label: 'menu.name', description: 'placeholder'},
                { id: 2, label: 'menu.unit_price', description: 'placeholder'},
                { id: 3, label: 'menu.count', description: 'placeholder'},
                { id: 4, label: 'menu.price', description: 'placeholder'},
                { id: 5, label: 'subtotal.subtotal_price', description: 'placeholder'},
                { id: 6, label: 'subtotal.tax_price', description: 'placeholder'},
                { id: 7, label: 'total.total_price', description: 'placeholder'},
                { id: 8, label: 'total.cash_price', description: 'placeholder'},
                { id: 9, label: 'total.credit_card_price', description: 'placeholder'},
                { id: 10, label: 'total.change_price', description: 'placeholder'},
                { id: 11, label: 'N/A (Not Applicable)', description: 'placeholder'}
                
            ],

            selected_boxes: this.$store.getters.getSelectedBoxes,
            image_box: this.$store.getters.getImageBoxes,

        }
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

        add() {
            this.$refs.form.validate()
            
            var id = this.labelTable.length
            this.labelTable.push({checked: false, id: id, label: this.label, description: this.description})
            
            this.label = ''
            this.description = ''

        },


        deleterow(id) {
            for (var label in this.labelTable) {
                if (this.labelTable[label].id === id) {
                    this.labelTable.splice(label, 1)
                }
            }
        },

        select() {
            for (var label in this.labelTable) {
                if (this.labelTable[label].checked === true) {
                    this.selection = this.labelTable[label].label
                }
            }
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

        checkAddButton() {
            console.log(this.selected_boxes)
            if (this.selected_boxes.length === 0) {
                return true
            }
            return false
        },

    },

    computed: {
        isDisabled() {
            return this.$store.getters.getSelectedBoxes.length === 0
        }
    },
}
</script>