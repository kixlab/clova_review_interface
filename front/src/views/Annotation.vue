<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-toolbar-title>HEADER</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <img alt="Vue logo" src="../assets/logo.png">
      <v-row>
        <v-col>
        <image-panel/>
        </v-col>
        <v-col>
          <labeling/>
          <linking/>
        </v-col>
      </v-row>
    </v-main>
  
    <v-footer
      dark
      indigo
      app
    >
      <v-spacer></v-spacer>

      <span class="white--text">&copy; 2019</span>
    </v-footer>

  </v-app>

</template>

<script>
// @ is an alias to /src
import ImagePanel from '@/components/ImagePanel.vue'
import Labeling from '@/components/Labeling.vue'
import Linking from '@/components/Linking.vue'

export default {
  name: 'Home',
  components: {
    ImagePanel,
    Linking,
    Labeling
  }
}
</script>
