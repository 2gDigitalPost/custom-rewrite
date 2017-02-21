import axios from 'axios'
import DatePicker from 'vue-datepicker'
import moment from 'moment'

import bus from '../../../bus'

export default {
  name: 'EditExpectedCompletionDate',
  props: ['currentDate', 'orderCode'],
  components: {
    DatePicker
  },
  data () {
    return {
      expectedCompletionDate: {
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
  methods: {
    saveChanges: function () {
      let self = this

      let apiURL = '/api/v1/order/' + self.orderCode
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'order_code': self.orderCode,
        'update_data': {
          'expected_completion_date': self.expectedCompletionDate.time
        }
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('order-updated')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancel: function () {
      bus.$emit('expected-completion-date-edit-cancel')
    }
  }
}