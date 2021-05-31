<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo lighten-1"
      dark
      dense
      fixed
    >
      <v-toolbar-title>Image Annotation (ID: {{this.$store.state.mturk_id}}, {{this.$store.state.image_order+1}} of 20 images)</v-toolbar-title>
      <v-spacer/>
      <instruction-button/>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
        <v-row>
          <Progress/>
        </v-row>
      <v-row align-content="start">
        <!-- COL1 - IMAGE LOADER -->
        <v-col cols="5">
          <v-row dense>
            <image-panel/>
          </v-row>
        </v-col>

        <!-- COL2 - ANNOTATION UI -->
        <v-col cols="7">
          <v-row dense>
            <box-selection-status/>
            <labeling/>
            <annotation-status/>
          </v-row>
        </v-col>
      </v-row>
      </v-container>
    </v-main>
  </v-app>

</template>

<script>
// @ is an alias to /src
import ImagePanel from '@/components/ImagePanel.vue'
import AnnotationStatus from '@/components/AnnotationStatus.vue'
import SubmitButton from '@/components/SubmitButton.vue'
import InstructionButton from '@/components/InstructionButton.vue'
import OverviewButton from '@/components/OverviewButton.vue'
import Labeling from '@/components/Labeling.vue'
import BoxSelectionStatus from '@/components/BoxSelectionStatus.vue'
import Progress from '@/components/Progress.vue'
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    Progress,
    ImagePanel,
    AnnotationStatus,
    SubmitButton,
    InstructionButton,
    OverviewButton,
    Labeling,
    BoxSelectionStatus
  },
  beforeCreate() {
    this.$helpers.isWrongAccess(this)

  },
  methods:{
    updateStatus(){
      const self=this;
      axios.get(self.$store.state.server_url+'/api/get-status/', {
        params: {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType
          }
        }).then(function (res) {
          self.$store.commit('update_status',res.data.status);
      })
    }
  },
  mounted(){
    this.updateStatus();
  }
}
</script>
