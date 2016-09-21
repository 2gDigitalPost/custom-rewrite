from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class InstructionsTemplateBuilderLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the InstructionsTemplateBuilder. Placed in the instructions_template table.
    """

    @staticmethod
    def get_launch_behavior(instructions_template_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var instructions_template_search_key = '%s';

    spt.tab.add_new('instructions_template_' + instructions_template_search_key, 'Instructions Template',
                    'widgets.InstructionsTemplateBuilderWdg', {'search_key': instructions_template_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % instructions_template_search_key
                    }
        return behavior

    def get_display(self):
        instructions_template_search_key = self.get_current_sobject().get_search_key()

        instructions_template_button = ButtonNewWdg(
            title='Instructions Template'.format(instructions_template_search_key), icon='WORK'
        )
        instructions_template_button.add_behavior(self.get_launch_behavior(instructions_template_search_key))

        return instructions_template_button
