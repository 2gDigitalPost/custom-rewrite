from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg


class InstructionsBuilderLoadPageWdg(BaseRefreshWdg):
    def get_display(self):
        div_wdg = DivWdg()

        div_wdg.add('<a href="http://localhost:5000/instructions_template_builder" target="_blank">Click here</a>')

        return div_wdg
