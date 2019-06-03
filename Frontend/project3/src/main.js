import Vue from 'vue'
import App from './App.vue'
var firebase = require("firebase");
require("firebase/firestore");

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

// Set the configuration for your app
var config = {
  apiKey: "AIzaSyCOr-NLa8btkEMh2yv__33OJ9CrgpvP9ts",
  authDomain: "project3-ml6.firebaseapp.com",
  projectId: "project3-ml6"
};
firebase.initializeApp(config);

var db = firebase.firestore();

export const myfunctions = {
  getData: function (collection) {
    db.collection(collection).get().then((docs) => {
      docs.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data()}`);
      })
    })
  } 
}