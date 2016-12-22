function get_component_count_options () {
    var options = [];

    for (var i = 1; i <= 20; i++) {
        options.push(i);
    }

    return options;
}

Vue.component('add-title', {
    template: '<div>\
            <h3>Are you adding a Movie, Trailer, Episode or a Season?</h3>\
            <select v-model="title_type">\
                <option>Movie</option>\
                <option>Trailer</option>\
                <option>Episode</option>\
                <option>Season</option>\
            </select>\
        </div>\
        '
});

var add_component_to_order = new Vue({
    el: '#add-components-to-order',
    data: {
        component_count: 0,
        component_count_options: get_component_count_options()
    }
});