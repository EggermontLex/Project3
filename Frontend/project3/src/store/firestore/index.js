const firebase = require('firebase/app')
require('firebase/firestore')
import { getters } from './getters'
import { actions } from './actions'
import { mutations } from './mutations'

var config = {
  apiKey: 'AIzaSyCOr-NLa8btkEMh2yv__33OJ9CrgpvP9ts',
  authDomain: 'project3-ml6.firebaseapp.com',
  projectId: 'project3-ml6'
}

firebase.initializeApp(config)

const state = {
  db: firebase.firestore()
}

const namespaced = true

export const firestore = {
  namespaced,
  state,
  getters,
  actions,
  mutations
}
