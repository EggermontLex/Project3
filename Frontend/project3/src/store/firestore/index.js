const firebase = require('firebase/app')
require('firebase/firestore')
import { getters } from './getters'
import { actions } from './actions'
import { mutations } from './mutations'
import { config } from './config'

firebase.initializeApp(config)

const state = {
  db: firebase.firestore(),
  isFiltered: false
}

const namespaced = true

export const firestore = {
  namespaced,
  state,
  getters,
  actions,
  mutations
}
