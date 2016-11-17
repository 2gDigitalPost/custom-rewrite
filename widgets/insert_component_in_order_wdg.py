import widgets.html_widgets
import widgets.input_widgets
from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SelectWdg, SubmitWdg

from common_tools.utils import get_instructions_select_wdg


def get_language_select_wdg():
    language_select_wdg = SelectWdg('language_code')
    language_select_wdg.set_id('language_code')
    language_select_wdg.add_style('display', 'inline-block')
    language_select_wdg.add_empty_option()

    language_search = Search('twog/language')
    languages = language_search.get_sobjects()

    languages = sorted(languages, key=lambda x: x.get_value('name'))

    for language in languages:
        language_select_wdg.append_option(language.get_value('name'), language.get_code())

    return language_select_wdg


def get_languages_checkboxes():
    languages_search = Search('twog/language')
    languages = languages_search.get_sobjects()

    languages_checkbox_table = Table()

    header_row = languages_checkbox_table.add_row()
    header = languages_checkbox_table.add_header(data='Languages', row=header_row)
    header.add_style('text-align', 'center')
    header.add_style('text-decoration', 'underline')

    for language in languages:
        checkbox = CheckboxWdg(name=language.get_code())

        checkbox_row = languages_checkbox_table.add_row()

        languages_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
        languages_checkbox_table.add_cell(data=language.get_value('name'), row=checkbox_row)

    return languages_checkbox_table


def get_title_select_wdg(width=300):
    title_select_wdg = SelectWdg('title_code')
    title_select_wdg.set_id('title_code')
    title_select_wdg.add_style('width', '{0}px'.format(width))
    title_select_wdg.add_empty_option()

    title_search = Search('twog/title')
    titles = title_search.get_sobjects()

    for title in titles:
        title_select_wdg.append_option(title.get_value('name'), title.get_code())

    return title_select_wdg


def get_season_select_wdg(width=300):
    season_select_wdg = SelectWdg('season_code')
    season_select_wdg.set_id('season_code')
    season_select_wdg.add_style('width', '{0}px'.format(width))

    season_search = Search('twog/season')
    seasons = season_search.get_sobjects()

    for season in seasons:
        season_select_wdg.append_option(season.get_value('name'), season.get_code())

    return season_select_wdg


def get_pipeline_select_wdg(search_type, width=300):
    """
    Given a search type, return a select widget with the pipelines available for that search type

    :param search_type: Search type as a string
    :param width: Width of the widget in pixels
    :return: SelectWdg
    """
    pipeline_select_wdg = SelectWdg('pipeline_code')
    pipeline_select_wdg.set_id('pipeline_code')
    pipeline_select_wdg.add_style('width', '{0}px'.format(width))
    pipeline_select_wdg.add_empty_option()

    pipeline_search = Search('sthpw/pipeline')
    pipeline_search.add_filter('search_type', search_type)
    pipelines = pipeline_search.get_sobjects()

    for pipeline in pipelines:
        pipeline_select_wdg.append_option(pipeline.get_value('name'), pipeline.get_code())

    return pipeline_select_wdg


class InsertComponentInOrderWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-component-in-order')

        outer_div.add(widgets.html_widgets.get_label_widget('Name'))
        outer_div.add(widgets.input_widgets.get_text_input_wdg('new_component_name', 400))

        outer_div.add(widgets.html_widgets.get_label_widget('Title'))
        outer_div.add(get_title_select_wdg(400))

        outer_div.add(widgets.html_widgets.get_label_widget('Language'))
        outer_div.add(get_language_select_wdg())

        outer_div.add(widgets.html_widgets.get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg('twog/component'))

        outer_div.add(widgets.html_widgets.get_label_widget('Instructions'))
        outer_div.add(get_instructions_select_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())
        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''

spt.app_busy.show("Saving...");

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#insert-component-in-order");
var new_component_values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var order_code = '%s';
var name = new_component_values.new_component_name;
var language_code = new_component_values.language_code;
var pipeline_code = new_component_values.pipeline_code;
var instructions_code = new_component_values.instructions_select;
var title_code = new_component_values.title_code;

var new_component = {
    'name': name,
    'order_code': order_code,
    'language_code': language_code,
    'pipeline_code': pipeline_code,
    'instructions_code': instructions_code,
    'title_code': title_code
}

server.insert('twog/component', new_component);

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
       self.parent_widget_search_key)
        }

        return behavior


class InsertComponentByLanguageWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-component-in-order-by-language')

        outer_div.add(widgets.html_widgets.get_label_widget('Name'))
        outer_div.add(widgets.input_widgets.get_text_input_wdg('new_component_name', 400))

        outer_div.add(widgets.html_widgets.get_label_widget('Title'))
        outer_div.add(get_title_select_wdg(400))

        outer_div.add(get_languages_checkboxes())

        outer_div.add(widgets.html_widgets.get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg('twog/component'))

        outer_div.add(widgets.html_widgets.get_label_widget('Instructions'))
        outer_div.add(get_instructions_select_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())
        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.app_busy.show("Saving...");

    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-component-in-order-by-language");
    var new_component_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var order_code = '%s';
    var name = new_component_values.new_component_name;
    var pipeline_code = new_component_values.pipeline_code;
    var instructions_code = new_component_values.instructions_select;
    var title_code = new_component_values.title_code;

    var languages = server.eval("@SOBJECT(twog/language)");

    for (var i = 0; i < languages.length; i++) {
        var language_code = languages[i].code;

        var language_checkbox_value = new_component_values[language_code];

        if (language_checkbox_value == "on") {
            var language_name = languages[i].name

            var new_component = {
                'name': name + ' - ' + language_name,
                'order_code': order_code,
                'language_code': language_code,
                'pipeline_code': pipeline_code,
                'instructions_code': instructions_code,
                'title_code': title_code
            }

            server.insert('twog/component', new_component);
        }
    }

    spt.app_busy.hide();
    spt.popup.close(spt.popup.get_popup(bvr.src_el));

    var parent_widget_title = '%s';
    var parent_widget_name = '%s';
    var parent_widget_search_key = '%s';

    spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior


class InsertComponentBySeasonWdg(BaseRefreshWdg):
    def init(self):
        self.order_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-component-in-order-by-season')

        outer_div.add(widgets.html_widgets.get_label_widget('Name'))
        outer_div.add(widgets.input_widgets.get_text_input_wdg('new_component_name', 400))

        outer_div.add(widgets.html_widgets.get_label_widget('Season'))
        outer_div.add(get_season_select_wdg(400))

        outer_div.add(get_languages_checkboxes())

        outer_div.add(widgets.html_widgets.get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg('twog/component'))

        outer_div.add(widgets.html_widgets.get_label_widget('Instructions'))
        outer_div.add(get_instructions_select_wdg())

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior())
        outer_div.add(submit_button)

        return outer_div

    def get_submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.app_busy.show("Saving...");

    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-component-in-order-by-season");
    var new_component_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var order_code = '%s';
    var pipeline_code = new_component_values.pipeline_code;
    var instructions_code = new_component_values.instructions_select;
    var season_code = new_component_values.season_code;

    var title_in_season_sobjects = server.eval("@SOBJECT(twog/title['season_code', '" + season_code + "'])");

    var languages = server.eval("@SOBJECT(twog/language)");

    for (var i = 0; i < languages.length; i++) {
        var language_code = languages[i].code;
        var language_checkbox_value = new_component_values[language_code];

        if (language_checkbox_value == "on") {
            var language_name = languages[i].name;

            for (var j = 0; j < title_in_season_sobjects.length; j++) {
                var title_code = title_in_season_sobjects[j].code;
                var title_name = title_in_season_sobjects[j].name;

                var new_component = {
                    'name': title_name + ' - ' + language_name,
                    'order_code': order_code,
                    'language_code': language_code,
                    'pipeline_code': pipeline_code,
                    'instructions_code': instructions_code,
                    'title_code': title_code
                }

                server.insert('twog/component', new_component);
            }
        }
    }

    spt.app_busy.hide();
    spt.popup.close(spt.popup.get_popup(bvr.src_el));

    var parent_widget_title = '%s';
    var parent_widget_name = '%s';
    var parent_widget_search_key = '%s';

    spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (self.order_sobject.get_code(), self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior
