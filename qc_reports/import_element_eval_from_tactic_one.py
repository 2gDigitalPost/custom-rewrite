from tactic_client_lib import TacticServerStub

from tactic.ui.common import BaseRefreshWdg

from pyasm.command import Command
from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg, PasswordWdg

from widgets.html_widgets import get_label_widget
from widgets.input_widgets import get_text_input_wdg


class ImportElementEvalFromTacticOneWdg(BaseRefreshWdg):
    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
// Return an object containing the element evaluation's values
var top = bvr.src_el.getParent("#element_eval_panel");
var report_values = spt.api.get_input_values(top, null, false);

var code = report_values['code'];
var username = report_values['username'];
var password = report_values['password'];

var server = TacticServerStub.get();

server.execute_cmd('qc_reports.GetTacticOneElementEvalCommand', {'element_eval_code': code,
                                                                 'username': username,
                                                                 'password': password});
    '''
        }

        return behavior

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('import-element-eval-form')

        page_label = "<div>Enter the unique code of the Element Evaluation you want to import. The code will be in a " \
                     "format like this: ELEMENT_EVAL00001 </br>" \
                     "When the process finishes, a popup will tell you the new code for the imported report. Make " \
                     "note of this code before closing the window."
        outer_div.add(page_label)

        outer_div.add(get_label_widget('Code'))
        outer_div.add(get_text_input_wdg('code', 300))

        outer_div.add(get_label_widget('Username'))
        outer_div.add(get_text_input_wdg('username', 400))

        outer_div.add(get_label_widget('Password'))
        password_input = PasswordWdg('password')
        outer_div.add(password_input)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.submit_button_behavior())
        outer_div.add(submit_button)

        return outer_div


class GetTacticOneElementEvalCommand(Command):
    def execute(self):
        element_eval_code = self.kwargs.get('element_eval_code')
        username = self.kwargs.get('username')
        password = self.kwargs.get('password')

        self.get_element_eval_from_tactic_one(element_eval_code, username, password)

    @staticmethod
    def get_element_eval_from_tactic_one(element_eval_code, username, password):
        server = TacticServerStub(server='http://tactic01.2gdigital.com', project='twog', user=username,
                                  password=password)

        element_eval = server.eval("@SOBJECT(twog/element_eval['code', '{0}'])".format(element_eval_code))
        element_eval_lines = server.eval("@SOBJECT(twog/element_eval_lines['element_eval_code', '{0}'])".format(element_eval_code))
        element_eval_audio_lines = server.eval("@SOBJECT(twog/element_eval_audio['element_eval_code', '{0}'])".format(element_eval_code))

        print(element_eval)
        print(element_eval_lines)
        print(element_eval_audio_lines)
