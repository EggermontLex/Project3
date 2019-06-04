import Vue from 'vue'
import App from './App.vue'
var firebase = require("firebase");
require("firebase/auth");
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

firebase.auth().signOut().then(function() {
  // Sign-out successful.
}).catch(function(error) {
  // An error happened.
});

firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in.
    var displayName = user.displayName;
    var email = user.email;
    var emailVerified = user.emailVerified;
    var photoURL = user.photoURL;
    var isAnonymous = user.isAnonymous;
    var uid = user.uid;
    var providerData = user.providerData;
    console.log('Logged in')
  } else {
    console.log('Signed out')
  }
});

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