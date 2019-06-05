import Vue from 'vue'
import App from './App.vue'
const firebase = require("firebase/app");
require("firebase/auth");
require("firebase/firestore");

Vue.config.productionTip = false

var config = {
  apiKey: "AIzaSyCOr-NLa8btkEMh2yv__33OJ9CrgpvP9ts",
  authDomain: "project3-ml6.firebaseapp.com",
  projectId: "project3-ml6"
};

firebase.initializeApp(config);

var db = firebase.firestore();

export const myFunctions = {
  getDocumentReference: function (collection, document) {
    return db.collection(collection).doc(document)
  },
  getData: function (collection) {
    return db.collection(collection).get().then((docs) => {
      console.log(docs)
      return docs
    })
  }  
}

new Vue({
  render: h => h(App)
}).$mount('#app')