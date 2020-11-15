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
      >
        Instruction
      </v-btn>
    </template>

    <v-card tile class="instruction">
      <v-card-title>
       <b># Instruction</b>
      </v-card-title>
      <v-card-text style="line-height: 1.8; color:black">
      1. Drag or click to select one or more 
        <svg width="12" height="12"><rect style="fill:transparent; stroke:red" width="12" height="12"/></svg>
        <span class="red-text"> red</span> box(es) on the image. The selected boxes become 
        <svg width="14" height="14"><rect style="fill:red; fill-opacity:0.1; stroke:red; stroke-width: 4px;" width="14" height="14"/></svg>
        <span style="color: red; font-weight: 900;"> solid red</span> box(es).<br>
      2. Choose one label that best describes the selected box(es) by clicking the 
        <v-btn small icon color="darkgrey"> <v-icon>check_circle</v-icon></v-btn> button. 
        The labeled boxes become  
        <svg width="13" height="12"><rect style="fill:grey; fill-opacity:0.4; stroke:grey;" width="13" height="12"/></svg>
        <span class="gray-text"> gray</span>.<br>
      3. The label status is shown on the right bottom corner. Please hover to see corresponding boxes and undo annotation if necessary. <br/>
      4. Once all boxes are labeled, click the <span class="bold-text">SUBMIT</span> button. A new set of image and boxes will be loaded.<br>
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

    mounted() {
        
    },

    methods: {

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