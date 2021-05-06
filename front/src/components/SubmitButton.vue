<template>
  <v-tooltip bottom :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :loading="loading"
        :disabled="disabled"
        color="error"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Submit
      </v-btn>
      </div>
    </template>
    Annotate all the boxes to submit!
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
      self.loading = true;

      // Polish annotation data
      var annotationData = []
      for (var group in self.annotated_boxes) {
        var tempGroup = self.annotated_boxes[group]
        var boxIDs = tempGroup.boxes.map((i) => {
          return i.box_id;
        })
        annotationData.push({boxes: boxIDs, label: tempGroup.label, group_id: group})
      }

      axios.post(self.$store.state.server_url + "/api/submit/", {
        mturk_id: self.$store.state.mturk_id,
        image_id: self.$store.state.image_order,
        annotationData: annotationData,
      }).then(function (res) {
        console.log(res)
        
        if (res.data.step >= 20) {
          self.$router.push('after-done')
        }
        self.$store.commit('set_step', res.data.step)

        self.$root.$emit('newImage');
        self.updateAnnotatedBoxes([[], "reset"])
        self.loading = false;
      })
      .catch(function(err) {
        self.loading = false;
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
