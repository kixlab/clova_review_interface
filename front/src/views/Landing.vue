<template>
<v-container>
  <v-row justify="center" align-content="center" align="center" class="up_margin">
    <div style="width: 80%;">
    <h1> Resolution Dashboard Interface </h1>
    Welcome to the resolution stage dashboard interface!<br><br>

    This task is conducted as a part of a research project in which we try to re-design the machine learning dataset generation process with crowdsourcing. 
    In this task, you will be asked to finalize the label set you made previously and resolve conflicts in the annotation phase.<br>

    <br/>
    <br/>
    
    <h4>Please enter your name to begin label set finalization.</h4>
    <v-form
      ref="form"
      v-model="valid"
      style="width:40%;"
    >
    <v-text-field
      v-model="turk_id"
      :rules="idRules"
      label="Name"
      required
    ></v-text-field>
    </v-form>
  
    </div>
  </v-row>
  

  <v-row justify="center" align="start" class="up_margin">
    <v-btn :disabled="!valid" @click="onClickNext('receipt')" color="indigo lighten-3" class="mr-4">
      Begin (receipt) <v-icon>mdi-arrow-right</v-icon>
    </v-btn>
    <v-btn :disabled="!valid" @click="onClickNext('event')" color="indigo lighten-3" class="mr-4">
      Begin (event flyer) <v-icon>mdi-arrow-right</v-icon>
    </v-btn>
  </v-row>
</v-container>
</template>


<script>
// @ is an alias to /src
import { mapActions, mapState } from "vuex";
import axios from 'axios';

export default {
  name: 'Landing',
  data: () => ({
    valid: true,
    turk_id: '',
    idRules: [
      v => !!v || 'Please enter a valid name',
    ]
  }),
  computed: {
    ...mapState(['mturk_id'])
  },
  methods: {
    ...mapActions(['setServerURL']),
    
    onClickNext: function(doctype) {
      const self = this;
      if (doctype==='receipt') {
        self.setServerURL('http://3.38.105.16:8000')
      }
      else if (doctype==='event') {
        self.setServerURL('http://52.78.121.66:8000') 
      }
      
      self.$refs.form.validate()
      self.$store.commit('set_mturk_id', self.turk_id.trim())

      axios.post(self.$store.state.server_url + '/dashboard/signup/', {
        username: self.$store.state.mturk_id,
        doctype: doctype
      })
      self.$router.push('../dashboard/'+doctype+'/')     
    },

    seeAnnotations: function(doctype, type) {
      const self = this;
      self.$router.push('../seeannots/'+doctype+'/'+type+'/0')
    }
    
  },
  mounted() {
    this.turk_id = this.mturk_id;
  }
}
</script>

<style scoped>
.up_margin {
  margin-top:2rem;
  text-align: left;
}
</style>
