import { getters } from './getters'
import { actions } from './actions'
import { mutations } from './mutations'

const state = {
  isLoggedIn: false
}

const namespaced = true

export const authentication = {
  namespaced,
  state,
  getters,
  actions,
  mutations
}
