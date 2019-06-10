import { getters } from './getters'
import { actions } from './actions'
import { mutations } from './mutations'

const state = {}

const namespaced = true

export const firestore = {
  namespaced,
  state,
  getters,
  actions,
  mutations
}
