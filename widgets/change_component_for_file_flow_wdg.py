from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg

from common_tools.utils import get_sobject_by_code, get_order_sobject_from_component_sobject,\
    get_component_sobjects_from_order_code


class ChangeComponentForFileFlowWdg(BaseRefreshWdg):
    def init(self):
        self.file_flow_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def get_display(self):
        div_wdg = DivWdg()

        current_code_div = DivWdg()
        component_code = self.file_flow_sobject.get('component_code')

        component_sobject = get_sobject_by_code('twog/component', component_code)
        current_code_div.add('Current Component set to {0} ({1})'.format(component_sobject.get('name'),
                                                                         component_code))

        order_sobject = get_order_sobject_from_component_sobject(component_sobject)
        component_sobjects_for_order = get_component_sobjects_from_order_code(order_sobject.get_code())

        component_select_wdg = SelectWdg()
        component_select_wdg.set_id('component_select')
        component_select_wdg.add_style('width: 165px;')
        component_select_wdg.add_empty_option()

        for component in component_sobjects_for_order:
            component_select_wdg.append_option(component.get('name'), component.get_code())

        div_wdg.add(current_code_div)
        div_wdg.add(component_select_wdg)

        return div_wdg
