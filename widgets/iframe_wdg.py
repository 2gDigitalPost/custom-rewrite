from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg


class IFrameWdg(BaseRefreshWdg):
    def init(self):
        self.location = self.kwargs.get('location')

    def get_display(self):
        if self.location:
            location = 'http://localhost:5000/#/' + self.location
        else:
            location = 'http://localhost:5000'

        iframe_div = DivWdg('<iframe src="{0}" style="width: 100%; height: 150%"></iframe>'.format(location))

        return iframe_div


class EnterANewOrderIFrameWdg(IFrameWdg):
    def init(self):
        self.location = 'orders/new'
