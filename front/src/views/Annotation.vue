<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-toolbar-title>Annotation</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
      <v-row>
        <!-- COL1 - IMAGE LOADER -->
        <v-col cols="6">
        <image-panel/>
        </v-col>

        <!-- COL2 - ANNOTATION UI -->
        <v-col cols="6">
          <v-row dense>
            <labeling-instruction/>
            <labeling/>
            <linking/>
          </v-row>
        </v-col>
      </v-row>

      <v-row justify='end'>
        <submit-button/>
      </v-row>
      </v-container>
      

    </v-main>
  
    <v-footer
      dark
      indigo
      app
    >
      <v-spacer></v-spacer>

      <span class="white--text">&copy; 2020</span>
    </v-footer>

  </v-app>

</template>

<script>
// @ is an alias to /src
import ImagePanel from '@/components/ImagePanel.vue'
import Labeling from '@/components/Labeling.vue'
import Linking from '@/components/Linking.vue'
import LabelingInstruction from '@/components/LabelingInstruction.vue'
import SubmitButton from '@/components/SubmitButton.vue'

export default {
  name: 'Home',
  components: {
    ImagePanel,
    Linking,
    Labeling,
    LabelingInstruction,
    SubmitButton
  }
}
</script>
