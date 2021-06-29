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
        <v-toolbar-title>Image Annotation {{id_field}}</v-toolbar-title>
      </v-app-bar>
      
      <v-main>
      <router-view/>
      </v-main>
    </v-app>
    </div>
  </div>
  
</template>

<script>
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


export default {
  name: 'app',
  created () {
      document.title = "Annotation";
  },
  data: () => (
    {
    id_field: ''}
    )
  ,
  mounted: function () {
    const self=this;
      axios.get(self.$store.state.server_url + "/api/check-user/", {
        }).then(function(res){
        var login_status=res.data.login_status;
        if(login_status){
          console.log(res);
          self.id_field='(ID: '+res.data.username+')'
        }
      });
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
