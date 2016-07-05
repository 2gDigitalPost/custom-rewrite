from pyasm.search import Search
from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg


class InstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.title_order_code = self.get_kwargs().get('title_order_code')

    @staticmethod
    def get_instruction_text_from_code(code):
        title_order_search = Search('twog/title_order')
        title_order_search.add_code_filter(code)
        title_order = title_order_search.get_sobject()

        return title_order.get('instructions')

    @staticmethod
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line[0] == '*':
                    formatted_line = '<h2>{0}</h2>'.format(line[2:])
                elif line[0] == '#':
                    formatted_line = '<h4>{0}</h4>'.format(line[2:])
                else:
                    formatted_line = '<p>{0}</p>'.format(line)

                output_html += formatted_line

        return output_html

    def get_display(self):
        div_wdg = DivWdg()

        instructions = self.get_instruction_text_from_code(self.title_order_code)

        if not instructions:
            instructions = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions))

        return div_wdg
