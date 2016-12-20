
var instructions_document_editor = new Vue({
  el: '#instructions_document_editor',
  data: {
    instructions_documents: [],
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

      var xhr = new XMLHttpRequest();

      xhr.open('POST', '/api/v1/titles/add');
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.send(JSON.stringify(data_to_submit));
    }
  }
});