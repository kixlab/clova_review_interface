<template>
  <v-dialog
    v-model="dialog"
    width="70%"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        outlined
        v-bind="attrs"
        v-on="on"
        @click="openInstruction"
      >
        Instruction
      </v-btn>
    </template>

    <v-card tile class="instruction">
      <v-card-title>
       <b># Instruction</b>
      </v-card-title>
      <v-card-subtitle> 
       <b>Please read the instruction below carefully before moving on to the task.</b>
      </v-card-subtitle>

      <v-card-text style="line-height: 1.8; color:black;">
        You are given <b style="color:blue;">21 images</b> to annotate in this task.
        Please click on the numbers on the top to move to each image. <br>
        You can move between images without finishing annotations for a single image. <br>
        However, in order to <b>submit</b> the task, you need to <b>finish labeling ALL the boxes.</b> <br> <br>


        <b>Note that the categories and the sub-categories given are <span style="color:blue;">not perfectly made</span></b>. <br>
        Thus, it is important that you clearly distinguish the <v-btn x-small outlined color="success" style='margin-right:1px;'>Exactly</v-btn> labels with the <v-btn x-small outlined color="warning">Can be</v-btn> labels. <br>
        Please label the boxes as <v-btn x-small outlined color="warning">Can be</v-btn> if you are unsure of your labeling. <br> <br> 


        For the labeling stage, please follow the below instruction - <br>

        1. <b>Drag or click to select</b> one or more 
          <svg width="12" height="12"><rect style="fill:transparent; stroke:red" width="12" height="12"/></svg>
          <span class="red-text"> red</span> box(es) on the image that represents <b>a single item</b>. The selected boxes become 
          <svg width="14" height="14"><rect style="fill:red; fill-opacity:0.1; stroke:red; stroke-width: 4px;" width="14" height="14"/></svg>
          <span style="color: red; font-weight: 900;"> solid red</span> box(es). <br/>
          <span style="marginLeft: 15px;"></span> To un-select the boxes, please click the <v-btn x-small color="secondary" depressed>Undo all selections</v-btn> button. 
           <br>
        2. <b>Choose one label</b> that best describes the selected box(es) and <b>click to label by stating if the label <span style="color:green;">Exactly</span> or <span style="color:orange;">Can be</span> describing the boxes</b>. 
          <br> <span style="marginLeft: 15px;"></span> The labeled boxes become  
          <svg width="13" height="12"><rect style="fill:grey; fill-opacity:0.4; stroke:grey;" width="13" height="12"/></svg>
          <span class="gray-text"> gray</span>.<br>
          

          
        3. You can find the labeled boxes on the right bottom panel. <b>Hover to see corresponding boxes</b> and undo labeling if necessary. <br/>
        4. Once all boxes in all images are labeled, <v-btn color="error" x-small>Submit</v-btn> button at the top right corner will be activated. <br/>
        <span style="marginLeft: 15px;"></span> Click to end the task and <b>receive the code to submit</b> on the MTurk page. <br><br>

        
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="dialog = false"
        >
          Exit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
    name: "InstructionButton",
    data() {
        return {
          dialog: false,
        };
    },

    methods: {
      openInstruction: function () {
        const self=this;
        self.dialog = true;
        self.$helpers.server_log(self, 'RI', [])
      }
    },
    mounted() {
      // this.dialog = true;
      this.openInstruction();
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
.blue-text {
  color:blue;
  font-weight: bold;
}
.gray-text {
  color:gray;
  font-weight: bold;
}
.bold-text {
  font-weight: bold;
}
</style>