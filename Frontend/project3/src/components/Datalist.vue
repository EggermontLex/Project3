<template>
    <div class="container_input">
        <label for="input" class="label">{{ label }}</label>
        <input name="input" list="browsers" class="input">
        <datalist id="browsers">
            <option v-for="id in Ids" :value="id" v-bind:key="id"/>
        </datalist>
    </div>
    
</template>
<script>
export default {
    name: 'Datalist',
    props:{
        label: String,
        Ids: Array
    }
}
</script>
<style scoped>
.container_input{
  border-bottom: 2px rgb(222,222,222) solid;
  padding: .75rem 0;
  margin-top: 8px;
}

.label{
  color: var(--color-primary-x-light);
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
  color: var(--color-primary-x-light);
  display:block;
  background: inherit;
}

.input::placeholder{
  color: inherit;
  opacity: 1;
}
</style>
