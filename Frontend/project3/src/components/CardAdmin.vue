<template>
  <div class="card">
    <div class="titles">
      <h1 class="title margin-left">Camera</h1>
      <h1 class="title margin-right">Trein</h1>
    </div>
    <div class="rows">
      <!--<CardAdminRow camera-id="Camera 1" :is-new="isNew" />
      <CardAdminRow camera-id="Camera 2" />-->
      <CardAdminRow
        v-for="device in devices"
        :key="device.id"
        :camera-id="device.name"
        :is-new="device.isNew"
        :all-train-ids="allTrainIds"
        :default-value="device.train"
      />
    </div>
  </div>
</template>

<script>
import CardAdminRow from './CardAdminRow.vue'
export default {
  name: 'CardAdmin',
  components: {
    CardAdminRow
  },
  props: {
    devices: {
      type: Array,
      default: () => []
    },
    allTrainIds: {
      type: Array,
      default: () => []
    }
  },
  data: function() {
    return {
      isNew: true
    }
  }
}
</script>

<style scoped>
.card {
  margin: 15px;
  width: 70%;
  padding: 49px;
  background-color: var(--color-neutral-xxxx-light);
  border-radius: 8px;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.2);
}
@media (max-width: 1200px) {
  .card {
    padding: 30px;
    width: calc(100% - 50px);
  }
}
@media (max-width: 576px) {
  .card {
    padding: 8px;
    width: 100%;
  }
}

.titles {
  display: flex;
  justify-content: space-between;
}
.title {
  width: 50%;
}
.margin-left {
  margin-left: 16px;
}
.margin-right {
  margin-right: 8px;
}
h1,
h2,
p {
  margin-bottom: 16px;
}

h1 {
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: var(--color-neutral-xxxx-dark);
  background-color: inherit;
}
</style>
