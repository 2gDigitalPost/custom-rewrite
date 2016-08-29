from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg, Table
from pyasm.widget import CheckboxWdg, SelectWdg, SubmitWdg

import order_builder_utils as obu


def get_language_select_wdg():
    language_select_wdg = SelectWdg('language_select')
    language_select_wdg.set_id('language_code')
    language_select_wdg.add_style('width', '300px')
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


class InsertComponentInPackageWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-component-in-package')

        outer_div.add(obu.get_label_widget('Name'))
        outer_div.add(obu.get_text_input_wdg('new_component_name', 400))

        outer_div.add(obu.get_label_widget('Language'))
        outer_div.add(get_language_select_wdg())

        outer_div.add(obu.get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg('twog/component'))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.package_sobject.get_code()))
        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(package_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-component-in-package");
    var new_component_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var package_code = '%s';
    var name = new_component_values.new_component_name;
    var language_code = new_component_values.language_code;
    var pipeline_code = new_component_values.pipeline_code;

    var new_component = {
        'name': name,
        'package_code': package_code,
        'language_code': language_code,
        'pipeline_code': pipeline_code
    }

    server.insert('twog/component', new_component);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % package_code
        }

        return behavior


class InsertComponentByLanguageWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-component-in-package')

        outer_div.add(obu.get_label_widget('Name'))
        outer_div.add(obu.get_text_input_wdg('new_component_name', 400))

        outer_div.add(get_languages_checkboxes())

        outer_div.add(obu.get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg('twog/component'))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.package_sobject.get_code()))
        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(package_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#insert-component-in-package");
    var new_component_values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var package_code = '%s';
    var name = new_component_values.new_component_name;
    var pipeline_code = new_component_values.pipeline_code;

    var languages = server.eval("@SOBJECT(twog/language)")

    for (var i = 0; i < languages.length; i++) {
        var language_code = languages[i].code;

        var language_checkbox_value = new_component_values[language_code];

        if (language_checkbox_value == "on") {
            var language_name = languages[i].name

            var new_component = {
                'name': name + ' - ' + language_name,
                'package_code': package_code,
                'language_code': language_code,
                'pipeline_code': pipeline_code
            }

            server.insert('twog/component', new_component);
        }
    }
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % package_code
        }

        return behavior
