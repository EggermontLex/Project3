<template>
  <div class="container_input">
    <label for="input" class="label">{{ label }}</label>
    <input
      name="input"
      list="datalist"
      class="input"
      placeholder="Alle treinen"
      :value="defaultValue"
      @input="$emit('input', $event.target.value)"
      @blur="onBlur($event.target.value)"
    />
    <datalist id="datalist">
      <option v-for="id in ids" :key="id" :value="id" />
    </datalist>
  </div>
</template>
<script>
export default {
  name: 'Datalist',
  props: {
    label: {
      type: String,
      default: 'Datalist'
    },
    ids: {
      type: Array,
      default: () => []
    },
    defaultValue: {
      type: String,
      default: ''
    },
    isAdmin: {
      type: Boolean,
      default: false
    },
    originalValue: {
      type: String,
      default: ''
    }
  },
  methods: {
    onBlur(newValue) {
      if (this.isAdmin) {
        if (newValue != this.originalValue) {
          this.$emit('updateDevice', newValue)
        }
      }
    }
  }
}
</script>
<style scoped>
.container_input {
  border-bottom: 2px rgb(222, 222, 222) solid;
  padding: 0.75rem 0;
  margin-top: 8px;
}

.label {
  color: var(--color-primary-x-light);
  font-size: 14px;
  font-weight: 500;
  width: 100%;
  display: block;
}

.input {
  width: 100%;
  border: none;
  font-size: 18px;
  font-weight: 500;
  height: 30px;
  line-height: 18px;
  color: var(--color-primary-x-light);
  display: block;
  background: inherit;
}

.input::placeholder {
  color: inherit;
  opacity: 1;
}
</style>
