<template>
  <v-tooltip left :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :loading="loading"
        :disabled="disabled"
        color="secondary"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Submit
      </v-btn>
      </div>
    </template>
    <span>Annotate all the boxes to submit!</span>
  </v-tooltip>
</template>

<script>
import axios from "axios";

export default {
  name: "ImagePanel",
  data() {
    return {
      loading: false,

      image_box: this.$store.getters.getImageBoxes,
      annotated_boxes: this.$store.getters.getAnnotatedBoxes,
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
    onSubmit: function() {
      const that = this;
      that.loading = true

      // Polish annotation data
      var annotationData = []
      for (var group in this.annotated_boxes) {
        var tempGroup = this.annotated_boxes[group]
        annotationData.push({boxes: tempGroup.boxes, label: tempGroup.label, group_id: group})
      }

      axios.post("http://localhost:8000/api/image/", {
        // user_id: "user_id",
        test: "testText"
      })
      .then(function (res) {
        console.log(res)
        that.loading = false
        alert("Server responded!!")
      })
      .catch(function(err) {
        that.loading = false
        alert(err);
      });
    }
  },

  computed: {
    disabled() {
      return !this.$store.getters.getIfAllBoxesAnnotated
    }
  }
}
</script>
