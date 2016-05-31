from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg, HtmlElement
from tactic.ui.input import TextInputWdg


class ExternalRejectionOnTitleOrderWdg(BaseRefreshWdg):
    def init(self):
        self.title_order_code = self.get_kwargs().get('code')

    def get_display(self):
        outer_div = DivWdg()
        outer_div.add_class('new-order-entry-form')
        outer_div.set_id('new-order-entry-form')

        # Set up the <input> widget for 'name'
        outer_div.add(HtmlElement.label('Name'))
        name_input = TextInputWdg(name='name')
        outer_div.add(name_input)