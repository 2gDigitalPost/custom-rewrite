from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class ElementEvalLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the OrderBuilderWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(element_eval_code):
        # TODO: Make this open a new tab rather than reloading the current one
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var element_eval_code = '%s';

    spt.api.load_tab('Element Evaluation', 'qc_reports.ElementEvalWdg', {'code': element_eval_code});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % element_eval_code
                    }
        return behavior

    def get_display(self):
        element_eval_code = self.get_current_sobject().get_code()

        element_eval_button = ButtonNewWdg(title='Element Evaluation for {0}'.format(element_eval_code), icon='WORK')
        element_eval_button.add_behavior(self.get_launch_behavior(element_eval_code))

        return element_eval_button
