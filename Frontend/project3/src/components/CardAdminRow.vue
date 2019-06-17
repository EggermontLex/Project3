<template>
  <div :class="[{ new_background_color: isNew }, cardAdminRowClass]">
    <div :class="[{ new_line_color: isNew }, newLineClass]"></div>
    <p class="card_admin_row_item padding-left">{{ cameraId }}</p>
    <Datalist
      v-model="datalist"
      label=""
      :ids="allTrainIds"
      class="datalist card_admin_row_item"
      :default-value="defaultValue"
      :is-admin="isAdmin"
      :original-value="defaultValue"
      @updateDevice="updateDevice"
    /><!--@change="onTreinIdChange"-->
  </div>
</template>

<script>
import Datalist from './Datalist.vue'
export default {
  name: 'CardAdminRow',
  components: {
    Datalist
  },
  props: {
    cameraId: {
      type: String,
      default: 'CameraID'
    },
    defaultValue: {
      type: String,
      default: ''
    },
    allTrainIds: {
      type: Array,
      default: () => []
    },
    isNew: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      newLineClass: 'new_line',
      cardAdminRowClass: 'card_admin_row',
      isAdmin: true,
      datalist: ''
    }
  },
  methods: {
    async updateDevice(value) {
      let data = { name: this.cameraId, train: value }
      await fetch(
        'https://europe-west1-project3-ml6.cloudfunctions.net/update_train',
        {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        }
      )
    }
  }
}
</script>

<style>
.card_admin_row {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  align-items: center;
  /*padding: 16px 8px;*/
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  height: 4rem;
}
.new_background_color {
  background-color: var(--color-primary-xx-light);
}
.new_background_color > p {
  font-weight: 900;
}
.card_admin_row:last-child {
  border-bottom: none;
}

.card_admin_row_item {
  width: 50%;
  padding: 0 !important;
  margin: 0 !important;
}
.padding-left {
  padding-left: 8px !important;
}
.new_line {
  width: 8px;
  height: 100%;
}
.new_line_color {
  background: var(--color-primary);
}
.datalist {
  margin-right: 16px !important;
  border-bottom: none !important;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
  background-color: var(--color-neutral-xxxx-light);
}
.datalist > input {
  color: var(--color-neutral-xxxx-dark) !important;
  padding-left: 16px;
  margin: 8px 0;
}

p {
  margin-bottom: 16px;
}
p {
  background-color: inherit;
  font-size: 18px;
  font-weight: 400;
  line-height: 30px;
  display: inline;
  margin-right: 8px;
  color: var(--color-neutral-xxxx-dark);
}
</style>
