var current_year = new Date().getFullYear();
var years = [''];

for (var year_iterator = current_year; year_iterator >= 1888; year_iterator--) {
  years.push(year_iterator);
}

var apiURL = 'http://www.omdbapi.com/?s=';
var counter = 0;

Vue.component('testing-component', {
  props: ['movietest'],
  template: ''
})

Vue.component('movie-checkbox', {
  props: ['movie'],
  template: '<input type="checkbox"/>'
})

Vue.component('title-info', {
  props: ['title'],
  template: ''
})

Vue.component('movie-item', {
  props: ['movie'],
  template: '\
    <li v-on:click="$emit(\'remove\')">\
      {{movie.Title}} ({{movie.Year}})\
    </li>\
  '
})

var app = new Vue({
  el: '#app',
  data: {
    name: '',
    type: 'Movie',
    year: '',
    year_options: years,
    movies: [],
    selected_id: '',
    selected_title: ''
  },
  watch: {
    selected_id: function (val) {
      var xhr = new XMLHttpRequest();
      var self = this;

      console.log(self.selected_id);

      xhr.open('GET', 'http://www.omdbapi.com/?i=' + self.selected_id);

      xhr.onload = function () {
        self.selected_title = JSON.parse(xhr.responseText);
        console.log(self.selected_title);
      }
      xhr.send();
    }
  },
  methods: {
    submitMessage: function() {
      var xhr = new XMLHttpRequest();
      var self = this;

      if (this.year !== '') {
        xhr.open('GET', apiURL + self.name + '&y=' + self.year + '&type=' + self.type);
      }
      else {
        xhr.open('GET', apiURL + self.name + '&type=' + self.type);
      }

      xhr.onload = function () {
        self.movies = JSON.parse(xhr.responseText).Search;
        console.log(self.movies);
      }
      xhr.send();
    },
    submitToTactic: function() {
      var title_to_submit = this.selected_title;
      console.log(title_to_submit);
      var data_to_submit = {};

      data_to_submit['actors'] = title_to_submit.Actors;
      data_to_submit['awards'] = title_to_submit.Awards;
      data_to_submit['country'] = title_to_submit.Country;
      data_to_submit['director'] = title_to_submit.Director;
      data_to_submit['genre'] = title_to_submit.Genre;
      data_to_submit['language'] = title_to_submit.Language;
      data_to_submit['metascore'] = title_to_submit.Metascore;
      data_to_submit['plot'] = title_to_submit.Plot;
      data_to_submit['poster'] = title_to_submit.Poster;
      data_to_submit['rated'] = title_to_submit.Rated;
      data_to_submit['released'] = title_to_submit.Released;
      data_to_submit['runtime'] = title_to_submit.Runtime;
      data_to_submit['name'] = title_to_submit.Title;
      data_to_submit['writer'] = title_to_submit.Writer;
      data_to_submit['year'] = title_to_submit.Year;
      data_to_submit['imdb_id'] = title_to_submit.imdbID;
      data_to_submit['imdb_rating'] = title_to_submit.imdbRating;
      data_to_submit['imdb_votes'] = title_to_submit.imdbVotes;

      var xhr = new XMLHttpRequest();
      var self = this;

      xhr.open('POST', '/api/v1/titles/add');

      /*xhr.onload = function () {
        self.movies = JSON.parse(xhr.responseText).Search;
        console.log(self.movies);
      }*/
      xhr.send();

      console.log(xhr.responseText);

      console.log(data_to_submit);
    }
  }
})
