import axios from 'axios'
import myDatepicker from 'vue-datepicker'
import moment from 'moment'

import bus from '../../bus'

export default {
  name: 'ProjectTemplateRequest',
  data () {
    return {
      name: null,
      description: null,
      dueDate: {
        time: ''
      },
      attachedFile: null,
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
      limit: [{
        type: 'fromto',
        from: moment().subtract(1, 'days').format('YYYY-MM-DD'),
      }]
    }
  },
  components: {
    'date-picker': myDatepicker,
  },
  methods: {
    submit: function () {
      let self = this

      let jsonData = {
        'token': localStorage.tactic_token,
        'project_template_request': {
          'name': self.name,
          'description': self.description,
          'due_date': self.dueDate.time
        }
      }

      let data = new FormData()
      data.append('json', JSON.stringify(jsonData))
      data.append('file', self.attachedFile)

      axios.post('/api/v1/project-templates/request', data, {
      })
      .then(function (response) {
        if (response.status === 200) {
          console.log(response)
          // Redirect to the order detail page
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    onFileChange: function (e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      
      this.attachedFile = e.target.files[0];

      this.createImage(files[0]);
    },
    createImage: function (file) {
      var image = new Image();
      var reader = new FileReader();
      var vm = this;

      reader.onload = (e) => {
        vm.image = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    removeImage: function (e) {
      this.image = '';
    }
  }
}