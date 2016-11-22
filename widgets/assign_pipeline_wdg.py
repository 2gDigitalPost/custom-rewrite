from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg

from widgets.html_widgets import get_label_widget


def get_pipeline_select_wdg(pipeline_code, search_type):
    pipeline_sel = SelectWdg('pipeline_select')
    pipeline_sel.set_id('pipeline_select')
    pipeline_sel.add_style('width', '135px')
    pipeline_sel.add_empty_option()

    pipeline_search = Search('sthpw/pipeline')
    pipeline_search.add_filter('search_type', search_type)
    pipelines = pipeline_search.get_sobjects()

    for pipeline in pipelines:
        pipeline_sel.append_option(pipeline.get_value('name'), pipeline.get_code())

    if pipeline_code:
        pipeline_sel.set_value(pipeline_code)

    return pipeline_sel


class AssignPipelineWdg(BaseRefreshWdg):
    def init(self):
        self.sobject = self.get_sobject_from_kwargs()

        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_submit_button_behavior(self, search_type):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    spt.app_busy.show('Saving...');

    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#assign-pipeline-wdg");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var sobject_code = '%s';
    var search_type = '%s';
    var pipeline_code = values.pipeline_select;

    // Build a search key using the sobject's code
    var search_key = server.build_search_key(search_type, sobject_code, 'twog');

    // Set up the kwargs to update the sobject's data
    var kwargs = {
        'pipeline_code': pipeline_code,
    }

    // Send the update to the server
    server.update(search_key, kwargs);

    spt.app_busy.hide();
    spt.popup.close(spt.popup.get_popup(bvr.src_el));

    // Reload the parent widget
    var parent_widget_title = '%s';
    var parent_widget_name = '%s';
    var parent_widget_search_key = '%s';

    spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (self.sobject.get_code(), search_type, self.parent_widget_title, self.parent_widget_name,
        self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('assign-pipeline-wdg')

        outer_div.add(get_label_widget('Pipeline'))

        pipeline_code = self.sobject.get_value('pipeline_code')

        # 'get_search_type' returns the full search type ('twog/component?project=twog'). Only need the first part.
        search_type = self.sobject.get_search_type().split('?')[0]

        outer_div.add(get_pipeline_select_wdg(pipeline_code, search_type))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(search_type))

        outer_div.add(submit_button)

        return outer_div
