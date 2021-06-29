import axios from 'axios'

export default {
    server_get(self, url, fn) {
      //console.log(self)
        axios.get(self.$store.state.server_url + url, {
        }).then(function (res) {
          fn.apply(this, [self, res])
        }).catch(function(err) {
          alert("Server is not responding\n" + err);
        });
    },
    server_post(self, url, fn) {
        axios.post(self.$store.state.server_url + url, {
        }).then(function (res) {
          fn.apply(this, [self, res])
        }).catch(function(err) {
          alert("Server is not responding\n" + err);
        });
    },
    server_log(self, type, box_ids, label='') {
      axios.post(self.$store.state.server_url + '/api/log/', {
        type: type,
        image_id : self.$store.state.image_order,
        box_ids : box_ids,
        label: label
      }).catch(function(err) {
        alert("Server is not responding\n" + err);
      });
  },
    isWrongAccess(self) {
      axios.get(self.$store.state.server_url + '/api/check-user/', {
      }).then(function(res){
        var login_status=res.data.login_status;
        if(!login_status){
          alert("You are not logged in. You will be redirected to the login page.")
          self.$router.push('landing');
        }
      });
    }
};