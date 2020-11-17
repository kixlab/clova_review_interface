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
       <b>Please read the instruction below very carefully before moving on to the task.</b>
      </v-card-subtitle>
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
        These are the five labeling categories.
        <ul>
          <li> <b style="color:red;">N/A</b>: If none of the labels below match with a box, you should select this label.</li>
          <li> <b style="color:blue;">Menu</b>: Labels that describe the menu on the receipt
            <ul>
              <li>name, unit price, count, price</li>
            </ul>
          <li> <b style="color:blue;">Subtotal</b>: The prices in this category will be added up to be the total price. 
            <ul>
              <li>subtotal price, tax price</li>
            </ul>
          <li> <b style="color:blue;">Total</b>: The total price is the amount that a customer should pay.
            <ul>
              <li>total price</li>
            </ul>
          </li>
          <li> <b style="color:blue;">Payment</b>: The price paid by each payment method
            <ul>
              <li>cash price, credit card price, change price</li>
            </ul>
          </li>
        </ul>
      3. You can check the labeled boxes on the image and on the box at the bottom. Hover to see corresponding boxes and undo annotation if necessary. <br/>
      4. Once all boxes are labeled, <span class="bold-text">SUBMIT</span> button at the top right corner will be activated. Click the button, and a new set of image and boxes will be loaded.<br>
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