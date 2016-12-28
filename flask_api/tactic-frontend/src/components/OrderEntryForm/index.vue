<template>
    <div>
        <input type="text" v-model="order_name" placeholder="Order Name" />
        <input type="text" v-model="po_number" placeholder="PO Number" />
        <client-select></client-select>
        <div class="card">
            <div class="row">
                <span>Due Date：</span>
                <date-picker :date="due_date" :option="option"></date-picker>
            </div>
            <div class="row">
                <span>Expected Completion Date：</span>
                <date-picker :date="expected_completion_date" :option="option"></date-picker>
            </div>
        </div>
    </div>
</template>
<style>
</style>
<script>
  import ClientSelect from './ClientSelect/index.vue'
  import myDatepicker from 'vue-datepicker'

  export default {
    name: 'OrderEntryForm',
    data () {
      return {
        order_name: '',
        po_number: '',

        due_date: {
          time: ''
        },
        expected_completion_date: {
          time: ''
        },

        option: {
          type: 'min',
          week: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
          month: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          format: 'YYYY-MM-DD HH:mm',
          placeholder: 'when?',
          inputStyle: {
            'display': 'inline-block',
            'padding': '6px',
            'line-height': '22px',
            'font-size': '16px',
            'border': '2px solid #fff',
            'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.2)',
            'border-radius': '2px',
            'color': '#5F5F5F'
          },
          color: {
            header: '#ccc',
            headerText: '#f00'
          },
          buttons: {
            ok: 'Ok',
            cancel: 'Cancel'
          },
          overlayOpacity: 0.5, // 0.5 as default
          dismissible: true // as true as default
        },
        timeoption: {
          type: 'min',
          week: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
          month: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          format: 'YYYY-MM-DD HH:mm'
        },
        multiOption: {
          type: 'multi-day',
          week: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
          month: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          format: 'YYYY-MM-DD HH:mm'
        }
      }
    },
    components: {
      'client-select': ClientSelect,
      'date-picker': myDatepicker
    }
  }
</script>
