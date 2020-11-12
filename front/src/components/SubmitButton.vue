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
import {mapActions} from 'vuex';

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
            this.image_box = this.$store.getters.getImageBoxes
        }
    })

  },
  methods: {
    ...mapActions(['setImageBoxes', 'updateAnnotatedBoxes',]),
    onSubmit: function() {
      const self = this;
      self.loading = true

      // Polish annotation data
      var annotationData = []
      for (var group in self.annotated_boxes) {
        var tempGroup = self.annotated_boxes[group]
        annotationData.push({boxes: tempGroup.boxes, label: tempGroup.label, group_id: group})
      }

      axios.post(self.$store.state.server_url + "/api/image/", {
        // user_id: "user_id",
        test: "testText"
      })
      .then(function () {
        self.$store.commit('update_image_count');
        axios.get(self.$store.getters.json_url).then(res => {
          self.setImageBoxes(res.data);
          self.updateAnnotatedBoxes([[], "reset"])
        })  
        self.loading = false;
        
        alert("Server responded!!")
      })
      .catch(function(err) {
        self.loading = false
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
