from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.web import DivWdg, HtmlElement

import order_builder.order_builder_utils as obu

from common_tools.utils import get_file_in_package_sobjects_by_package_code,\
    get_file_sobjects_from_file_in_package_sobjects
from widgets.input_widgets import get_task_status_select_wdg


class PackageInspectWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()

    def get_files_list(self):
        outer_div = DivWdg()

        file_in_package_sobjects = get_file_in_package_sobjects_by_package_code(self.package_sobject.get_code())
        file_sobjects = get_file_sobjects_from_file_in_package_sobjects(file_in_package_sobjects)

        files_unordered_html_list = HtmlElement.ul()

        for file_sobject, file_in_package_sobject in zip(file_sobjects, file_in_package_sobjects):
            task_sobject = file_in_package_sobject.get_all_children('sthpw/task')[0]

            file_li = HtmlElement.li()
            file_li.add(file_sobject.get('file_path') + ' - ' + task_sobject.get('status'))

            change_status_button = ButtonNewWdg(title='Change Status')
            change_status_button.add_behavior(
                obu.get_load_popup_widget_with_reload_behavior(
                    'Change Status', 'widgets.ChangeStatusWdg', task_sobject.get_search_key(),
                    'Package', 'widgets.PackageInspectWdg', self.package_sobject.get_search_key()
                )
            )
            change_status_button.add_style('display', 'inline-block')

            file_li.add_style('vertical-align', 'center')
            file_li.add(change_status_button)

            files_unordered_html_list.add(file_li)

        outer_div.add(files_unordered_html_list)

        return outer_div

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var package_code = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#package_inspect_" + package_code);
var values = spt.api.get_input_values(containing_element, null, false);

var task_status = values["task_status_select"];

// Set up an object to hold the data
var kwargs = {
    'status': task_status
}

server.update(task_search_key, kwargs);

spt.app_busy.hide();

spt.api.load_tab('Task', 'widgets.TaskInspectWdg', {'search_key': task_search_key});
''' % (self.package_sobject.get_code())
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('package_inspect_{0}'.format(self.package_sobject.get_code()))

        task_sobject = self.package_sobject.get_all_children('sthpw/task')[0]

        outer_div.add(HtmlElement.h4('<u>Status</u>'))
        outer_div.add(get_task_status_select_wdg(task_sobject))

        outer_div.add(HtmlElement.h4('<u>Files</u>'))
        outer_div.add(self.get_files_list())

        return outer_div
