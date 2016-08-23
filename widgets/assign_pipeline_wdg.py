from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg

from order_builder.order_builder_utils import get_label_widget, get_widget_header


def get_pipeline_select_wdg():
    pipeline_sel = SelectWdg('pipeline_select')
    pipeline_sel.set_id('pipeline_select')
    pipeline_sel.add_style('width', '135px')
    pipeline_sel.add_empty_option()

    pipeline_search = Search('sthpw/pipeline')
    pipeline_search.add_filter('search_type', 'twog/title_order')
    pipelines = pipeline_search.get_sobjects()

    for pipeline in pipelines:
        pipeline_sel.append_option(pipeline.get_value('name'), pipeline.get_code())

    return pipeline_sel


def get_submit_behavior():
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
    }

    return behavior


def get_submit_widget():
    submit_button = SubmitWdg('Submit')
    submit_button.add_behavior(get_submit_behavior())

    return submit_button


class AssignPipelineWdg(BaseRefreshWdg):
    def init(self):
        title_order_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('assign-pipeline-wdg')

        page_label = 'Assign Pipeline'
        outer_div.add(get_widget_header(page_label))

        outer_div.add(get_label_widget('Pipeline'))
        outer_div.add(get_pipeline_select_wdg())

        outer_div.add(get_submit_widget())

        return outer_div