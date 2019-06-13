<template>
  <div :class="[{ new_background_color: isNew }, cardAdminRowClass]">
    <div :class="[{ new_line_color: isNew }, newLineClass]"></div>
    <p class="card_admin_row_item padding-left">{{ cameraId }}</p>
    <Datalist label="" ids="trainIds" class="datalist card_admin_row_item" />
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
    isNew: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      trainIds: ['Trein1', 'Trein2'],
      newLineClass: 'new_line',
      cardAdminRowClass: 'card_admin_row'
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
