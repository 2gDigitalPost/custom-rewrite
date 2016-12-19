var order_creator = new Vue({
    el: '#order-creator',
    data: {
        name: '',
        client: '',
        client_options: [],
        division: '',
        division_options: [],
        due_date: '',
        expected_completion_date: '',
        po_number: ''
    },
    methods: {
        loadClients: function() {
            $.get('/api/v1/clients', function (response) {
                for (var i = 0; i < response.clients.length; i++) {
                    this.client_options.push({text: response.clients[i].name, value: response.clients[i].code});
                }
            }.bind(this));
        },
        submit: function() {
            var data_to_send = {};

            data_to_send['name'] = this.name;
            data_to_send['client'] = this.client;
            data_to_send['division'] = this.division;
            data_to_send['due_date'] = this.due_date;
            data_to_send['expected_completion_date'] = this.expected_completion_date;
            data_to_send['po_number'] = this.po_number;

            $.ajax({
                url: '/api/v1/orders/add',
                type: 'POST',
                data: JSON.stringify(data_to_send),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(message) {
                    alert(message);
                }
            });
        }
    },
    beforeMount: function() {
        this.loadClients();
    },
    watch: {
        client: function(val) {
            $.get('/api/v1/divisions/' + val, function (response) {
                console.log(response.divisions);

                this.division_options = [];

                for (var i = 0; i < response.divisions.length; i++) {
                    Vue.set(this.division_options, i, {text: response.divisions[i].name, value: response.divisions[i].code});
                }

            }.bind(this));
        }
    }
});