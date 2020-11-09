<template>
  <v-col cols="12">
    <v-card tile class="instruction">
      <v-card-title>
       <b># Instruction</b>
      </v-card-title>
      <v-card-text style="line-height: 1.8">
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
    </v-card>
  </v-col>
</template>

<script>

export default {
  name: 'LabelingInstruction'
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