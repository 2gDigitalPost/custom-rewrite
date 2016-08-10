from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class MetaDataLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the MetaDataWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(metadata_eval_code):
        # TODO: Make this open a new tab rather than reloading the current one
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var metadata_eval_code = '%s';

    spt.api.load_tab('MetaData Evaluation', 'qc_reports.MetaDataReportWdg', {'search_type': 'twog/metadata_report', 'code': metadata_eval_code});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % metadata_eval_code
                    }
        return behavior

    def get_display(self):
        metadata_eval_code = self.get_current_sobject().get_code()

        metadata_eval_button = ButtonNewWdg(title='MetaData Evaluation for {0}'.format(metadata_eval_code), icon='WORK')
        metadata_eval_button.add_behavior(self.get_launch_behavior(metadata_eval_code))

        return metadata_eval_button
