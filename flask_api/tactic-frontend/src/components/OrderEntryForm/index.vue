<template>
    <div>
        <input type="text" v-model="order_name" placeholder="Order Name" />
        <client-select></client-select>
    </div>
</template>
<style>
</style>
<script>
  import ClientSelect from './ClientSelect/index.vue'

  export default {
    name: 'OrderEntryForm',
    data () {
      return {
        order_name: ''
      }
    },
    components: {
      'client-select': ClientSelect
    }
  }
</script>
