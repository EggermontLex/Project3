<template>
    <div class="container_input">
        <label for="input" class="label">{{ label }}</label>
        <input :type="type" class="input" name="input" :placeholder="text_placeholder">
    </div>
</template>

<script>
export default {
  name: 'Input',
  props: {
    label: String,
    text_placeholder: String,
    type: String
  }  
}
</script>

<style scoped>
.container_input{
  border-bottom: 2px rgb(222,222,222) solid;
  padding: .75rem 0;
}

.label{
  color: #ddf1fa;
  font-size: 14px;
  font-weight: 500;
  width: 100%;
  display:block;
}

.input{
  width: 100%;
  border: none;
  font-size: 18px;
  font-weight: 500;
  height: 30px;
  line-height: 18px;
  color: #ddf1fa;
  display:block;
  background: inherit;
}

.input::placeholder{
  color: inherit;
  opacity: 1;
}
</style>
