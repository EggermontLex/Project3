import Vue from 'vue'
import App from './App.vue'
import VueApexCharts from 'vue-apexcharts'
const firebase = require('firebase/app')
require('firebase/auth')
require('firebase/firestore')

Vue.config.productionTip = false

Vue.component('apexchart', VueApexCharts)

var config = {
  apiKey: 'AIzaSyCOr-NLa8btkEMh2yv__33OJ9CrgpvP9ts',
  authDomain: 'project3-ml6.firebaseapp.com',
  projectId: 'project3-ml6'
}

firebase.initializeApp(config)

var db = firebase.firestore()

export const myFunctions = {
  getDocumentReference: function(collection, document) {
    return db.collection(collection).doc(document)
  },
  getCollectionDocs: function(collection) {
    return db
      .collection(collection)
      .get()
      .then(docs => {
        return docs
      })
  },
  getTrainHistory: function(trainId, hours) {
    let d = new Date()
    d = new Date(d.setHours(d.getHours() - hours))
    return db
      .collection('history')
      .where('train', '==', trainId)
      .where('timestamp', '>', d)
      .get()
      .then(docs => {
        return docs
      })
  }
}

new Vue({
  render: h => h(App)
}).$mount('#app')
