import Vue from 'vue'

export const mutations = {
  setFilteredState(state, isFiltered) {
    Vue.set(state, 'isFiltered', isFiltered)
  }
}
