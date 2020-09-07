<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo"
      dark
      absolute
    >
      <v-toolbar-title>Image Annotation</v-toolbar-title>
      <v-spacer/>
      <end-exp-button/>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
      <v-row dense>
        <labeling-instruction/>
      </v-row>
      <v-divider/>
      <v-row align-content="start">
        <!-- COL1 - IMAGE LOADER -->
        <v-col cols="6">
          <v-row dense>
            <image-panel/>
          </v-row>
        </v-col>

        <!-- COL2 - ANNOTATION UI -->
        <v-col cols="6">
          <v-row dense>
            <labeling/>
            <annotation-status/>
          </v-row>
          <v-row justify='end'>
            <submit-button/>
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
import LabelingInstruction from '@/components/LabelingInstruction.vue'
import SubmitButton from '@/components/SubmitButton.vue'
import EndExpButton from '@/components/EndExpButton.vue'
import Labeling from '@/components/Labeling.vue'

export default {
  name: 'Home',
  components: {
    ImagePanel,
    AnnotationStatus,
    LabelingInstruction,
    SubmitButton,
    EndExpButton,
    Labeling,
  }
}
</script>
