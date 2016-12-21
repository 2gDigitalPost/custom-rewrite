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
    el: '#add-title-to-tactic',
    data: {
        title_type: '',
        title_search_name: '',
        season_number: '',
        episode_number: '',
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
        searchForEpisode: function() {
            var omdbURL = 'http://www.omdbapi.com/?t=' + this.title_search_name + '&Season=' + this.season_number + '&Episode=' + this.episode_number;

            $.get(omdbURL, function(response) {

            }.bind(this));

        },
        searchForSeason: function() {
            var omdbURL;
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
        searchOMDbForEpisode: function() {

        },
        searchOMDbForSeason: function() {

        },
        addTitleToTactic: function() {
            var title_to_submit = this.omdb_selected_title;
            console.log(title_to_submit);
            var data_to_submit = {};

            data_to_submit['actors'] = title_to_submit.Actors;
            data_to_submit['awards'] = title_to_submit.Awards;
            data_to_submit['country'] = title_to_submit.Country;
            data_to_submit['director'] = title_to_submit.Director;
            data_to_submit['genre'] = title_to_submit.Genre;
            data_to_submit['language'] = title_to_submit.Language;
            data_to_submit['metascore'] = parseInt(title_to_submit.Metascore);
            data_to_submit['plot'] = title_to_submit.Plot;
            data_to_submit['poster'] = title_to_submit.Poster;
            data_to_submit['rated'] = title_to_submit.Rated;
            data_to_submit['released'] = title_to_submit.Released;
            data_to_submit['runtime'] = title_to_submit.Runtime;
            data_to_submit['name'] = title_to_submit.Title;
            data_to_submit['writer'] = title_to_submit.Writer;
            data_to_submit['year'] = title_to_submit.Year;
            data_to_submit['imdb_id'] = title_to_submit.imdbID;
            data_to_submit['imdb_rating'] = parseFloat(title_to_submit.imdbRating.replace(/,/g, ''));
            data_to_submit['imdb_votes'] = parseInt(title_to_submit.imdbVotes);
            data_to_submit['type'] = title_to_submit.Type;

            $.ajax({
                url: '/api/v1/titles/add',
                type: 'POST',
                data: JSON.stringify(data_to_submit),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(message) {
                    if (message.status == 200) {
                        location.reload();
                    }
                }
            });
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
        },
        title_not_in_tactic_results: function() {
            // If the user declares that the Title is not in Tactic, unselect any of the search results the user may
            // have clicked on
            var self = this;

            this.selected_title_code = '';
        }
    }
});
