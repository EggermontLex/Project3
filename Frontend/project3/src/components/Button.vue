<template>
    <button type="button" name="button" class="button">{{text}}</button>
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
  padding: 14px 45px;
  border-radius: 5px;
  box-shadow: 0 2px 0 rgba(0,0,0,.2) ;
  color: #006ab3;
  border: none;
  font-family: CircularStd;
  font-size: 18px;
  font-weight: 700;
}

</style>

