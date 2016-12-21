function get_year_options() {
    var current_year = new Date().getFullYear();
    var years = [''];

    for (var year_iterator = current_year; year_iterator >= 1888; year_iterator--) {
        years.push(year_iterator);
    }

    return years;
}

Vue.component('title-item', {
    props: ['title'],
    template: '\
        <li v-on:click="$emit(\'title-selected\')">\
            {{title.name}} ({{title.code}})\
        </li>\
    '
});

Vue.component('omdb-title-item', {
    props: ['title'],
    template: '\
        <li v-on:click="$emit(\'omdb-title-selected\')">\
            {{ title.name }} ({{ title.year }}) - {{ title.imdbID }}\
        </li>\
    '
});

var add_component_by_title = new Vue({
    el: '#add-component-by-title',
    data: {
        title_type: '',
        title_search_name: '',
        tactic_title_searched: false,
        tactic_title_search_results: [],
        title_not_in_tactic_results: false,
        selected_title_code: '',
        search_omdb_or_manual_entry: '',
        omdb_search_year: '',
        year_options: get_year_options(),
        omdb_searched: false,
        omdb_found_titles: [],
        omdb_selected_id: '',
        omdb_selected_title: ''
    },
    methods: {
        searchForTitle: function() {
            $.get('/api/v1/title/name/' + this.title_search_name, function(response) {
                this.tactic_title_searched = true;
                this.tactic_title_search_results = [];

                for (var i = 0; i < response.titles.length; i++) {
                    Vue.set(this.tactic_title_search_results, i, {name: response.titles[i].name, code: response.titles[i].code});
                }
            }.bind(this));
        },
        searchOMDbForTitle: function() {
            var omdbURL;

            if (this.title_type.toLowerCase() === 'movie') {
                omdbURL = 'http://www.omdbapi.com/?s=' + this.title_search_name + '&type=' + this.title_type;
            }
            else if (this.title_type.toLowerCase() === 'episode') {
                omdbURL = 'http://www.omdbapi.com/?s=' + this.title_search_name + '&type=' + this.title_type;
            }

            if (this.omdb_search_year !== '') {
                omdbURL += '&y=' + this.omdb_search_year;
            }

            $.get(omdbURL, function(response) {
                this.omdb_searched = true;
                this.omdb_found_titles = [];

                // The json object returned from OMDb always returns a "Response" string, set to either "True" or
                // "False".
                if (response.Response.toLowerCase() === 'true') {
                    var found_titles = response.Search;

                    for (var i = 0; i < found_titles.length; i++) {
                        Vue.set(this.omdb_found_titles, i, {name: found_titles[i].Title, year: found_titles[i].Year, imdbID: found_titles[i].imdbID});
                    }
                }
            }.bind(this));
        },
        addTitleToTactic: function() {

        },
        submit: function() {
            var data_to_send = {};

            data_to_send['name'] = this.name;
            data_to_send['division_code'] = this.division;
            data_to_send['due_date'] = this.due_date;
            data_to_send['expected_completion_date'] = this.expected_completion_date;
            data_to_send['po_number'] = this.po_number;
            data_to_send['status'] = 'pending';

            $.ajax({
                url: '/api/v1/orders/add',
                type: 'POST',
                data: JSON.stringify(data_to_send),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(message) {
                    window.location.replace("/orders/" + message['order_code'] + "/add_component_by_title");
                }
            });
        }
    },
    watch: {
        omdb_selected_id: function() {
            var self = this;
            var omdbURL = 'http://www.omdbapi.com/?i=' + this.omdb_selected_id;

            $.get(omdbURL, function(response) {
                if (response.Response.toLowerCase() === 'true') {
                    self.omdb_selected_title = response;
                }
            });
        }
    }
});