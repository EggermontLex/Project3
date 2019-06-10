import Vue from 'vue'
import Vuex from 'vuex'
import { firestore } from './firestore'
import { authentication } from './authentication'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    firestore,
    authentication
  }
})

export default store
