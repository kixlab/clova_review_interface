<template>
  <v-col cols="12">
    <v-card tile class="instruction">
      <h2> ## Instruction </h2>
      1. Drag to select one or more <span class="red-text">red</span> box(es) from the image. The selected boxes become colored <span class="blue-text">blue</span>.<br>
      2. Choose one label that best describes the selected box(es). The labeled boxes become colored <span class="gray-text">gray</span>.<br>
      3. Once all boxes are labeled, click <span class="bold-text">SUBMIT</span> button. A new image and boxes will be loaded.<br>

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