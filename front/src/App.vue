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
        <v-toolbar-title>Resolution Dashboard {{id_field}}</v-toolbar-title>
        <v-spacer/>
        <v-btn depressed outlined style="margin-right: 5px" @click="newLink('receipt')" 
        :disabled="this.$router.currentRoute.params.docType === 'receipt'">
          Receipt
        </v-btn>
        <v-btn depressed outlined @click="newLink('event')"
        :disabled="this.$router.currentRoute.params.docType === 'event'">
          Event flyer
        </v-btn>
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
      document.title = "Resolution Dashboard";
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
  },
  methods: {
    newLink: function(type) {
      const self = this;
      //console.log(self.$router.currentRoute.params.docType)
      if (self.$router.currentRoute.params.docType !== type) {
        self.$router.push('../imageview/'+type)
      }
      
    }
  },

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
