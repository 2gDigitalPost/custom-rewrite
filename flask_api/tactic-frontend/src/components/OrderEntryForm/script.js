import bus from '../../bus'
import ClientSelect from './ClientSelect/index.vue'
import myDatepicker from 'vue-datepicker'

import axios from 'axios'

export default {
  name: 'OrderEntryForm',
  data () {
    return {
      order_name: '',

      due_date: {
        time: ''
      },
      expected_completion_date: {
        time: ''
      },

      selected_division: null,

      order_submitted: false,
      submitted_order_code: null,

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
  },
  methods: {
    addOrderToTactic: function() {
      var self = this

      axios.post('/api/v1/orders', 
        JSON.stringify({
          'name': self.order_name,
          'division_code': self.selected_division,
          'expected_completion_date': self.expected_completion_date.time,
          'due_date': self.due_date.time
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Redirect to the order detail page
            self.order_submitted = true
            self.submitted_order_code = response.data.order_code
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    divisionSelected: function (division) {
      var self = this
      self.selected_division = division
    },
    redirectToOrderDetail: function () {
      this.$router.push('/orders/' + this.submitted_order_code)
    },
    redirectToAddTitle: function () {
      this.$router.push('/orders/' + this.submitted_order_code + '/titles/add')
    },
    refreshPage: function () {
      this.$router.go(this.$router.currentRoute)
    }
  },
  created() {
    bus.$on('division-selected', this.divisionSelected)
  },
  destroyed() {
    bus.$off('division-selected', this.divisionSelected)
  },
}