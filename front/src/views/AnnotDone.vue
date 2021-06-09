<template>
  <v-container fill-height>
    <v-row justify="center">
    <v-col style="text-align: center;">
      <v-card>
        <v-card-text>
          All the deferred annotations with 'EXACTLY' labels are saved as regular annotations! 
          In the next phase, you will review items that you marked as 'N/A' or 'CAN BE'.
        </v-card-text>
         <v-btn
            @click="onClickNext"
            color="deep-purple accent-2"
            class="mr-4"
            style="margin-left: auto;"
            large
          >
            Next
          </v-btn>
      </v-card>
      <br>
      <v-divider/>
    </v-col>
    </v-row>
  </v-container>
</template>


<script>
export default {
  name: 'AnnotDone',
  methods: {
    onClickNext: function () {
      const self = this;

      self.$helpers.server_get(self, "/api/instr-done", 
        function(self, res){ // eslint-disable-line no-unused-vars
          self.$router.push('doctypelist/')
        })
    }
  },
  beforeCreate() {
    this.$helpers.isWrongAccess(this)
  },
  created: function () {
    setTimeout(() => {
      this.passOneMinute = true
    }, 2*1000);
    setInterval(() => {
      this.time_now += 1
    }, 1000);
  }
}
</script>

<style scoped>
.v-responsive__content {
  align-content: center !important;
  display: flex !important;;
}

.v-card__text {
  color:black !important;
}

.endPanel {
  margin-left: auto;
  margin-right: auto;
  width: 70%;
  background-color: white !important;
}

.reds {
  color:red;
  background-color:white !important;
}
</style>