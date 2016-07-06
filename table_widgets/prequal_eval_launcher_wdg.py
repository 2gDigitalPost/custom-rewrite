from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class PrequalEvalLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the PreQualEvalWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(prequal_eval_code):
        # TODO: Make this open a new tab rather than reloading the current one
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var prequal_eval_code = '%s';

    spt.api.load_tab('PreQual Evaluation', 'qc_reports.PrequalEvalWdg', {'search_type': 'twog/prequal_evaluation', 'code': prequal_eval_code});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % prequal_eval_code
                    }
        return behavior

    def get_display(self):
        prequal_eval_code = self.get_current_sobject().get_code()

        prequal_eval_button = ButtonNewWdg(title='PreQual Evaluation for {0}'.format(prequal_eval_code), icon='WORK')
        prequal_eval_button.add_behavior(self.get_launch_behavior(prequal_eval_code))

        return prequal_eval_button
