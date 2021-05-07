<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%">
        <b> 2. Choose a label that best describes the <span class="red-text">selected box(es)</span>.</b> 
      </v-card-title>
      
      <v-card-subtitle class='text-left'>
        There are <b style="color:blue;">10 categories</b> and <b style="color:red;">N/A</b>. Please scroll down to take a look at all of them.
      </v-card-subtitle>
      
      <v-card-text> 
        <v-row>
          <v-col :cols="4" style="text-align:left;">
            Category
            <v-list >
              <v-list-item-group
                mendatory
                active-class="border"
                color="indigo"
              >
                <v-list-item v-for="(category, index) in table" :key='index' @click="selectCategory(category)">
                  <b>{{category}}</b>
                </v-list-item>
                <v-list-item v-if="isAdding">
                  <v-text-field label="new category" id='newCat'></v-text-field>
                  <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="addCategory()">+ add</v-btn>
                  <v-btn x-small outlined color="red" v-on:click.stop="cancelAdd()">X</v-btn>
                </v-list-item>
                <v-list-item v-if="!isAdding" v-on:click.stop="getCategory()"><b>+</b> add</v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>

          <v-col :cols="8" style="text-align:left;">
            Sub-category
             <v-list>
              <v-list-item-group
                active-class="border"
                color="indigo"
              >
                <v-list-item v-for="(item, index) in labelTable.filter(e=>e.label == category)" :key="index" @click="annotate(item)">
                  <b>{{item.sublabel}} </b>: {{item.description}}
                </v-list-item>
                <v-list-item v-if="isAddingSub">
                  <v-text-field label="new subcategory" id='newSubCat'></v-text-field>
                  :
                  <v-text-field label="description" id='newDesc'></v-text-field>
                  <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="addSubCategory()">+ add</v-btn>
                  <v-btn x-small outlined color="red" v-on:click.stop="cancelAddSub()">X</v-btn>
                </v-list-item>
                <v-list-item v-if="isCategorySelected&&(!isAddingSub)" v-on:click.stop="getSubCategory()"><b>+</b> add</v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
        </v-row>
         <!-- <v-row>
          <v-col class="text-left">
            <div v-for="category in table" :key="category" style="padding: 4px;">
              <v-menu open-on-hover right offset-x>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="text-none"
                    color="normal"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ category }}
                  </v-btn>
                </template>
                <v-list dense>
                  <v-list-item
                    v-for="(item, index) in labelTable.filter(e => e.label == category)"
                    :key="index"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-btn class="text-none" color="normal" small text @click="clicked(item.sublabel); annotate(item)" :disabled=isDisabled>
                        {{ item.sublabel }}
                        </v-btn>
                      </v-list-item-title>
                      <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
              <br/>
            </div>
          </v-col>
        </v-row>

        <v-row>
          <v-col class="text-left">
            <v-autocomplete
              clearable
              dense
              filled
              :items="labelTable"
              label="Search for the label.."
            >
              <template v-slot:selection="data">
                {{ data.item.label.concat(' - ', data.item.sublabel) }}
              </template>
              <template v-slot:item="data">
                
              </template>
            </v-autocomplete>
          </v-col>
        </v-row> -->

        <!-- <v-row>
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
                              <v-icon>check_circle</v-icon>
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
        </v-row> -->
      </v-card-text>

    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'Labeling',
  data() {
    var categories=[]
    var subcats=[]
    switch(this.$route.params.docType){ 
      case 'receipt':
        categories=['menu', 'subtotal', 'total', 'payment']
        subcats=[
          { id: 1, label: 'menu', sublabel: 'id', description: 'ID of the menu'},
          { id: 2, label: 'menu', sublabel: 'name', description: 'Name of the menu'},
          { id: 3, label: 'menu', sublabel: 'unit price', description: 'Unit price of the menu'},
          { id: 4, label: 'menu', sublabel: 'count', description: 'Number of the menu consumed'},
          { id: 5, label: 'menu', sublabel: 'price', description: 'Total price of the menu'},
          { id: 6, label: 'subtotal', sublabel: 'menu count', description: 'Number of unique menus'},
          { id: 7, label: 'subtotal', sublabel: 'item count', description: 'Number of items'},
          { id: 8, label: 'subtotal', sublabel: 'price', description: 'Subotal price excluding tax'},
          { id: 9, label: 'subtotal', sublabel: 'service charge', description: 'Service charge'},
          { id: 10, label: 'subtotal', sublabel: 'tax price', description: 'Tax price'},
          { id: 11, label: 'total', sublabel: 'total price', description: 'Total price'},
          { id: 12, label: 'payment', sublabel: 'cash payment', description: 'Price paid by cash'},
          { id: 13, label: 'payment', sublabel: 'credit card payment', description: 'Price paid by credit card'},
          { id: 14, label: 'payment', sublabel: 'change', description: 'Amount of change received'},
      ]
      break;
      case 'resume':
        categories=['personal info', 'employment', 'education', 'experience', 'publication', 'committee', 'awards']
        subcats=[
          { id: 1, label: 'personal info', sublabel: 'name', description: 'Name of the person'},
          { id: 2, label: 'personal info', sublabel: 'office address', description: 'Address of the office'},
          { id: 3, label: 'personal info', sublabel: 'office no', description: 'Phone number of the office'},
          { id: 4, label: 'personal info', sublabel: 'job title', description: 'Title of the current job'},
          { id: 5, label: 'personal info', sublabel: 'institution', description: 'Institution that the person works at'},
          { id: 6, label: 'personal info', sublabel: 'birthplace', description: 'Birthplace of the person'},
          { id: 7, label: 'personal info', sublabel: 'birthdate', description: 'Birthdate of the person'},
          { id: 8, label: 'personal info', sublabel: 'research interest', description: 'Field that the person is working on or interested in'},
          { id: 9, label: 'employment', sublabel: 'title', description: 'Title of the job'},
          { id: 10, label: 'employment', sublabel: 'institution', description: 'Institution that the person worked at'},
          { id: 11, label: 'employment', sublabel: 'location', description: 'Location of the institution'},
          { id: 12, label: 'employment', sublabel: 'year', description: 'Dates of the experience'},
          { id: 13, label: 'education', sublabel: 'degree', description: 'Degree that the person has'},
          { id: 14, label: 'education', sublabel: 'institution', description: 'Institution or school that the person received the degree'},
          { id: 15, label: 'education', sublabel: 'location', description: 'Location of the institution'},
          { id: 16, label: 'education', sublabel: 'major', description: 'Major field of study for the degree'},
          { id: 17, label: 'education', sublabel: 'graduation year', description: 'Year that the person received the degree'},
          { id: 18, label: 'experience', sublabel: 'title', description: 'Title of the experience'},
          { id: 19, label: 'experience', sublabel: 'institution', description: 'Title of the experience'},
          { id: 20, label: 'experience', sublabel: 'location', description: 'Location of the experience'},
          { id: 21, label: 'experience', sublabel: 'role description', description: 'Role description of the experience'},
          { id: 22, label: 'experience', sublabel: 'year', description: 'Dates of the experience'},
          { id: 23, label: 'publication', sublabel: 'title', description: 'Publication title'},
          { id: 24, label: 'publication', sublabel: 'year', description: 'Publication year'},
          { id: 25, label: 'publication', sublabel: 'venue', description: 'Journal or conference the paper was published'},
          { id: 26, label: 'publication', sublabel: 'authors', description: 'Author list of the publication'},
          { id: 27, label: 'committee', sublabel: 'title', description: 'Title of the committee that the person belongs to'},
          { id: 28, label: 'committee', sublabel: 'organization', description: 'Organization of the committee'},
          { id: 29, label: 'committee', sublabel: 'year', description: 'Dates that the person served in the committee'},
          { id: 30, label: 'awards', sublabel: 'title', description: 'Title of the award'},
          { id: 31, label: 'awards', sublabel: 'institution', description: 'Institution that gave the award'},
          { id: 32, label: 'awards', sublabel: 'yaer', description: 'Dates that the person received the award'},
      ]

    }
    return {
      selection: [],
      labelTable: subcats,
      selected_boxes: this.$store.getters.getSelectedBoxes,
      image_box: this.$store.getters.getImageBoxes,
      table: categories,
      category:'',
      subcategory:'',
      addcat: false,
      addsubcat: false,
    }
  },
  mounted: function () {
    this.$store.subscribeAction((action) => {
      if (action.type === 'updateImageBoxes') {
          this.image_box = this.$store.getters.getImageBoxes
      }
    })
  },

  methods: {
      ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes']),
      ...mapGetters(['getImageBoxes']),

      selectCategory(selectedCategory){
        this.category=selectedCategory;
        this.addsubcat=false;
      },

      getCategory(){
        this.category='';
        this.addcat=true;
      },
      getSubCategory(){
        this.subcategory='';
        this.addsubcat=true;
      },

      addCategory(){
        this.addcat=false;
        console.log(this.addcat);
        var newcat=document.getElementById('newCat').value;
        this.table.push(newcat);        
      },
       addSubCategory(){
        this.addsubcat=false;
        var newsubcat=document.getElementById('newSubCat').value;
        var newdesc=document.getElementById('newDesc').value;
        this.labelTable.push({label: this.category, sublabel: newsubcat, description: newdesc});        
      },
      cancelAdd(){
        this.addcat=false;
      },

      add() {
        this.$refs.form.validate()
        
        var id = this.labelTable.length
        this.labelTable.push({checked: false, id: id, label: this.label, description: this.description})
        
        this.label = '';
        this.description = '';
      },

      annotate(item) {
        const imageBox = this.getImageBoxes()//this.image_box
        var group = []
        var label = item.label + "." + item.sublabel

        for (var box in imageBox) {
            if (imageBox[box].selected === true) {
                var currBox = this.image_box[box]
                currBox.label = label
                currBox.selected = false
                currBox.annotated = true
                group.push(currBox)
            }
        }

        this.$helpers.server_log(this, 'CL', group.map((i) => {return i.box_id}), label)
        this.updateImageBoxes(this.image_box)
        this.updateAnnotatedBoxes([{label: item.label + " - " + item.sublabel, boxes: group}, "add"])

      },

      clicked(label) {
        console.log("Clicked", label)
      }
  },
  computed: {
    isDisabled() {
        return this.$store.getters.getSelectedBoxes.length === 0
    },
    isCategorySelected(){
      return (this.category!='')
    },
    isSubSelected(){
      return (this.subcategory!='')
    },
    isAdding(){
      return (this.addcat)
    },
    isAddingSub(){
      return (this.addsubcat)
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