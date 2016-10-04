from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class PackageInspectLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the TaskInspectWdg. Placed in the task table.
    """

    @staticmethod
    def get_launch_behavior(task_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var package_search_key = '%s';

    spt.tab.add_new('package_inspect_' + package_search_key, 'Package', 'widgets.PackageInspectWdg',
                    {'search_key': package_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % task_search_key
                    }
        return behavior

    def get_display(self):
        package_search_key = self.get_current_sobject().get_search_key()

        package_inspect_button = ButtonNewWdg(
            title='Inspect Task'.format(package_search_key), icon='WORK'
        )
        package_inspect_button.add_behavior(self.get_launch_behavior(package_search_key))

        return package_inspect_button
