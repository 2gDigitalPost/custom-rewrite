from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class TaskInspectLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the TaskInspectWdg. Placed in the task table.
    """

    @staticmethod
    def get_launch_behavior(task_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var task_search_key = '%s';

    spt.tab.add_new('task_inspect_' + task_search_key, 'Task', 'widgets.TaskInspectWdg',
                    {'search_key': task_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % task_search_key
                    }
        return behavior

    def get_display(self):
        task_search_key = self.get_current_sobject().get_search_key()

        task_inspect_button = ButtonNewWdg(
            title='Inspect Task'.format(task_search_key), icon='WORK'
        )
        task_inspect_button.add_behavior(self.get_launch_behavior(task_search_key))

        return task_inspect_button
