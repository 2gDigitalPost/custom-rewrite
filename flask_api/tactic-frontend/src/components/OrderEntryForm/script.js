import axios from 'axios'
import myDatepicker from 'vue-datepicker'

import ClientSelect from './ClientSelect/index.vue'
import PurchaseOrderSelect from '../PurchaseOrderSelect/index.vue'
import PurchaseOrderEntryForm from '../PurchaseOrderEntryForm/index.vue'

import bus from '../../bus'

export default {
  name: 'OrderEntryForm',
  data () {
    return {
      order_name: '',
      
      purchaseOrderOption: null,
      newPurchaseOrderNumber: null,
      selectedPurchaseOrderCode: null,

      due_date: {
        time: ''
      },
      expected_completion_date: {
        time: ''
      },

      selectedDivision: null,

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
    'date-picker': myDatepicker,
    PurchaseOrderSelect,
    PurchaseOrderEntryForm
  },
  methods: {
    addOrderToTactic: function() {
      let self = this

      let jsonData = {
        'token': localStorage.tactic_token,
        'order': {
          'name': self.order_name,
          'division_code': self.selectedDivision,
          'expected_completion_date': self.expected_completion_date.time,
          'due_date': self.due_date.time
        }
      }

      if (self.purchaseOrderOption === 'new') {
        jsonData['new_purchase_order'] = {'name': self.newPurchaseOrderNumber, 'division_code': self.selectedDivision}
      }
      else if (self.purchaseOrderOption === 'existing') {
        jsonData['existing_purchase_order'] = {'code': self.selectedPurchaseOrderCode, 'division_code': self.selectedDivision}
      }

      axios.post('/api/v1/orders', JSON.stringify(jsonData), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
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
      self.selectedDivision = division
    },
    purchaseOrderNumberChanged: function (number, exists) {
      if (exists) {
        this.newPurchaseOrderNumber = null
      }
      else {
        this.newPurchaseOrderNumber = number
      }
    },
    purchaseOrderSelected: function (code) {
      this.selectedPurchaseOrderCode = code
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
    bus.$on('po-number-changed', this.purchaseOrderNumberChanged)
    bus.$on('purchase-order-selected', this.purchaseOrderSelected)
  },
  destroyed() {
    bus.$off('division-selected', this.divisionSelected)
    bus.$off('po-number-changed', this.purchaseOrderNumberChanged)
    bus.$off('purchase-order-selected', this.purchaseOrderSelected)
  },
}