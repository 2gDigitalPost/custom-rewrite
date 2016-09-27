from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class ElementEvalLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the ElementEvalWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(element_eval_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var element_eval_search_key = '%s';

    spt.tab.add_new('element_eval_' + element_eval_search_key, 'Element Evaluation', 'qc_reports.ElementEvalWdg',
                    {'search_key': element_eval_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % element_eval_search_key
                    }
        return behavior

    def get_display(self):
        element_evaluation = self.get_current_sobject()

        element_eval_button = ButtonNewWdg(title='Element Evaluation for {0}'.format(element_evaluation.get_code()),
                                           icon='WORK')
        element_eval_button.add_behavior(self.get_launch_behavior(element_evaluation.get_search_key()))

        return element_eval_button
