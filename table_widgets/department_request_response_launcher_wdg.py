from tactic.ui.common import BaseTableElementWdg
from tactic.ui.widget import ButtonNewWdg


class DepartmentRequestResponseLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the DepartmentRequestResponseWdg. Placed in the task table.
    """

    @staticmethod
    def get_launch_behavior(department_request_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var department_request_search_key = '%s';

    spt.panel.load_popup('department_request_response', 'widgets.DepartmentRequestResponseWdg',
                         {'search_key': department_request_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % department_request_search_key
                    }
        return behavior

    def get_display(self):
        department_request = self.get_current_sobject()

        response_button = ButtonNewWdg(title='Response for {0}'.format(department_request.get_code()), icon='WORK')
        response_button.add_behavior(self.get_launch_behavior(department_request.get_search_key()))

        return response_button
