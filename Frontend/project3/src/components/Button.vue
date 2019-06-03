<template>
    <button type="button" name="button" class="button">{{ text }}</button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    text: String
  }   
}
</script>

<style scoped>
.button{
  background-color: #FFF;
  padding: 14px 0;
  border-radius: 5px;
  box-shadow: 0 2px 0 rgba(0,0,0,.2) ;
  color: #006ab3;
  border: none;
  font-size: 18px;
  font-weight: 700;
  width: 100%;
}
</style>
