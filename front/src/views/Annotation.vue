<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-toolbar-title>Annotation - {{user_id}}</v-toolbar-title>
    </v-app-bar>

    <v-main class="noPadding">
      <v-container>
      <v-row align-content="start">
        <!-- COL1 - IMAGE LOADER -->
        <v-col cols="6">
          <labeling-instruction/>
          <image-panel/>
        </v-col>

        <!-- COL2 - ANNOTATION UI -->
        <v-col cols="6">
          <v-row dense>
            
            <label-list/>
            <labeled-boxes/>
          </v-row>
          <v-row justify='end'>
            <submit-button/>
          </v-row>
        </v-col>
      </v-row>

      </v-container>
      

    </v-main>
  
    <v-footer
      dark
      indigo
      app
    >
      <v-spacer></v-spacer>
      <v-col cols="6">
        <v-row justify="center">
          <page-buttons/>
        </v-row>
      </v-col>
      
      <v-col cols="3">
        <v-row>
          <v-spacer></v-spacer>
          <end-exp-button/>
          <span class="white--text"> &copy; 2020</span>
        </v-row>
      </v-col>

      
    </v-footer>

  </v-app>

</template>

<script>
// @ is an alias to /src
import PageButtons from '@/components/PageButtons.vue'
import ImagePanel from '@/components/ImagePanel.vue'
import LabelList from '@/components/LabelList.vue'
import LabeledBoxes from '@/components/LabeledBoxes.vue'
import LabelingInstruction from '@/components/LabelingInstruction.vue'
import SubmitButton from '@/components/SubmitButton.vue'
import EndExpButton from '@/components/EndExpButton.vue'

export default {
  name: 'Home',
  components: {
    PageButtons,
    ImagePanel,
    LabelList,
    LabeledBoxes,
    LabelingInstruction,
    SubmitButton,
    EndExpButton,
  },
  props: {
    user_id: {
      type: String,
      default: null
    }
  },
  beforeMount () {
    if (this.user_id.length < 1) throw new Error('User ID must be passed in URL!')
    return true
  }
}
</script>

<style scoped>
.noPadding {
  padding-top: 0px !important;
}
</style>