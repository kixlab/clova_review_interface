<template>
  <div id="app">
    <div v-if="$route.name === 'Annotation' || $route.name === '404'">
      <router-view/>
    </div>
    <div v-else>
      <v-app>
      <v-app-bar app
        color="indigo lighten-1"
        dark
        dense
        fixed>
        <v-toolbar-title>Resolution Interface {{id_field}}</v-toolbar-title>
      </v-app-bar>
      
      <v-main>
      <router-view/>
      </v-main>
    </v-app>
    </div>
  </div>
  
</template>

<script>
export default {
  name: 'app',
  created () {
      document.title = "Annotation";
  },
  computed: {
    id_field: function () {
      var mturk_id = this.$store.state.mturk_id;
      if (mturk_id === null) {
        return ''
      }
      else {
        return '(ID : ' + mturk_id + ')'
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
