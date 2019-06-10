<template>
  <div class="container_input">
    <label for="input" class="label">{{ label }}</label>
    <input
      :value="text_input"
      @input="$emit('input', $event.target.value)"
      :type="type"
      class="input"
      name="input"
      :placeholder="text_placeholder"
    />
  </div>
</template>

<script>
export default {
  name: 'Input',
  props: {
    label: String,
    text_placeholder: String,
    type: String,
    text_input: String
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

input[type='date']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  display: none;
}
input[type='time']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  display: none;
}
</style>
