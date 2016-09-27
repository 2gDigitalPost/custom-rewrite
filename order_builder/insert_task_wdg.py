import widgets.html_widgets
import widgets.input_widgets
from tactic_client_lib import TacticServerStub

from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextAreaInputWdg

from pyasm.command import Command
from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import MultiSelectWdg, SubmitWdg

import order_builder_utils as obu


class InsertTaskWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('insert-task-in-component')

        outer_div.add(widgets.input_widgets.get_text_input_wdg('process'))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.component_sobject.get_code()))

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(component_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
spt.app_busy.show("Saving...");

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#insert-task-in-component");
var new_package_values = spt.api.get_input_values(containing_element, null, false);

// Get the form values
var component_code = '%s';
var process = new_package_values.process;

// Get the user's login name
var env = spt.Environment.get();
var login = env.user;

// Set up the object for the new task entry.
var new_task = {
    'process': process,
    'search_code': component_code,
    'search_type': 'twog/component',
    'login': login
}

server.execute_cmd('order_builder.insert_task_wdg.AddTaskToComponentCbk', new_task);

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));
''' % (component_code)
        }

        return behavior


class AddTaskToComponentCbk(Command):
    '''Callback to add a standalone task to a component'''

    def execute(self):
        process = self.kwargs.get('process')
        component_code = self.kwargs.get('search_code')
        login = self.kwargs.get('login')

        if process and component_code and login:
            self.add_task_to_component(process, component_code, login)

    def add_task_to_component(self, process, component_code, login):
        server = TacticServerStub.get()

        component_search = Search('twog/component')
        component_search.add_code_filter(component_code)
        component = component_search.get_sobject()

        server.insert('sthpw/task', {'process': process, 'login': login}, parent_key=component.get_search_key())
