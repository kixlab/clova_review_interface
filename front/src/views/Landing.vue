<template>
<v-container>
  <v-row justify="center" align-content="center" align="center" class="up_margin">
    <div style="width: 80%;">
    <h1> Resolution Dashboard Interface </h1>
    Welcome to the resolution stage dashboard interface!<br><br>

    This task is conducted as a part of a research project in which we try to re-design the machine learning dataset generation process with crowdsourcing. 
    In this task, you will be asked to finalize the label set you made previously and resolve conflicts in the annotation phase.<br>

    <br/>

    You can either choose to ~~~.

    <br/> <br/>
    
    <h4>Please enter your name to begin label set and annotation finalization.</h4>
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
  <v-divider/>
    </div>
  </v-row>

  <v-row justify="center" align="start" class="up_margin">
    <v-btn
      :disabled="!valid"
      @click="onClickNext"
      
      color="indigo lighten-2"
      class="mr-4"
    >
      Begin 
      <v-icon>
        mdi-arrow-right
      </v-icon>
    </v-btn>
  </v-row>
</v-container>
</template>


<script>
// @ is an alias to /src
import { mapState } from "vuex";
//import axios from 'axios';

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
    /* Got from the mturk interface
    onClickNext: function () {
      const self = this;
      self.$refs.form.validate()
      self.$store.commit('set_mturk_id', self.turk_id.trim())
      axios.post(self.$store.state.server_url + '/api/signup/', {
        username: self.$store.state.mturk_id,
      }).then( function(res){
//        self.$store.commit('set_mturk_id', self.turk_id.trim())
        if(res.data.status=='instruction'){
          self.$router.push('/instruction/')
        } else{
          if(res.data.status=='annotation'){
            self.$store.commit('set_start_image_no', 0);
            self.$router.push('/resolution/'+res.data.doctype+'/image/')
          }else{
            self.$store.commit('update_status', new Array(300).fill(false));
            self.$router.push('../informed-consent/')                    }
        }
      });
    },
    */

    onClickNext: function() {
      const self = this;
      self.$refs.form.validate()
      self.$store.commit('set_mturk_id', self.turk_id.trim())
      self.$router.push('../dashboard/')     
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
