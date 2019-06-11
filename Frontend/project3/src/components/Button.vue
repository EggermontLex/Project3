<template>
  <button type="button" name="button" class="button">{{ text }}</button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    text: {
      type: String,
      default: 'Button'
    }
  }
}
</script>

<style scoped>
.button {
  background-color: var(--color-neutral-xxxx-light);
  padding: 14px 0;
  border-radius: 5px;
  box-shadow: var(--box-shadow);
  color: var(--color-primary);
  border: none;
  font-size: 18px;
  font-weight: 700;
  width: 100%;
}
.button:hover,
.button:active {
  box-shadow: var(--box-shadow_hover);
  color: var(--color-primary-xx-dark);
}
</style>
