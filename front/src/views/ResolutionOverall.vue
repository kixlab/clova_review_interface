<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo lighten-1"
      dark
      dense
      fixed
    >
      <v-toolbar-title>Resolution Interface - Overall Level (ID: {{this.$store.state.mturk_id}}, {{this.$store.state.image_order+1}} of 300 images)</v-toolbar-title>
      <v-spacer/>
      <!--<instruction-button/>-->
      <submit-button/>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
        <!--
        <v-row>
          <Progress style="paddingBottom: 20px"/>
        </v-row>
        -->
      <v-row align-content="start">
        <!-- COL1 - IMAGE LOADER -->
        <!--
        <v-col cols="1">
          <v-row dense>
            <image-panel/>
          </v-row>
        </v-col>
        -->

        <!-- COL2 - ANNOTATION UI -->
        <v-col cols="12">
          <v-row dense>
            <overall-label/>
            <!--<box-selection-status/>
            <deferred-annotation/>
            <deferred-annotation-status/>-->
          </v-row>
        </v-col>
      </v-row>
      </v-container>
    </v-main>
  </v-app>

</template>

<script>
// @ is an alias to /src
//import ImagePanel from '@/components/ImagePanel.vue'
//import DeferredAnnotationStatus from '@/components/DeferredAnnotationStatus.vue'
import SubmitButton from '@/components/SubmitButton.vue'
//import InstructionButton from '@/components/InstructionButton.vue'
//import OverviewButton from '@/components/OverviewButton.vue'
//import DeferredAnnotation from '@/components/DeferredAnnotation.vue'
//import BoxSelectionStatus from '@/components/BoxSelectionStatus.vue'
//import Progress from '@/components/Progress.vue'
import axios from 'axios'
//import SubmitButton from '../components/SubmitButton.vue'
import OverallLabel from '@/components/OverallLabel.vue'
export default {
  name: 'Home',
  components: {
    //Progress,
    //ImagePanel,
    //DeferredAnnotationStatus,
    SubmitButton,
    //InstructionButton,
    //OverviewButton,
    //DeferredAnnotation,
    //BoxSelectionStatus,
    OverallLabel
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
