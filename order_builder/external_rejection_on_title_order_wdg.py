from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg


class ExternalRejectionOnTitleOrderWdg(BaseRefreshWdg):
    def init(self):
        self.title_order_code = self.get_kwargs().get('code')

    def get_display(self):
        div = DivWdg()

        return div