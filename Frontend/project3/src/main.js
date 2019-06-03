import Vue from 'vue'
import App from './App.vue'
var firebase = require("firebase/app");

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

// Set the configuration for your app
var config = {
  apiKey: "AIzaSyCOr-NLa8btkEMh2yv__33OJ9CrgpvP9ts",
  authDomain: "project3-ml6.firebaseapp.com",
  //storageBucket: "bucket.appspot.com"
};
firebase.initializeApp(config);
