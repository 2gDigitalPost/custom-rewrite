from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg

from widgets.delivery_task_inspect_wdg import DeliveryTaskInspectWdg
from widgets.task_inspect_wdg import TaskInspectWdg


class GenericTaskInspectWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()

    def get_display(self):
        div_wdg = DivWdg()
        div_wdg.set_id('outer_task_inspect_{0}'.format(self.task_sobject.get_code()))

        if self.task_sobject.get('process').lower() == 'edel: deliver':
            div_wdg.add(DeliveryTaskInspectWdg(search_key=self.task_sobject.get_search_key()))
        else:
            div_wdg.add(TaskInspectWdg(search_key=self.task_sobject.get_search_key()))

        return div_wdg
