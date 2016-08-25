from pyasm.search import Search
from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg


class ComponentInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

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

        instructions_code = self.component_sobject.get('instructions_code')

        if instructions_code:
            instructions_search = Search('twog/instructions')
            instructions_search.add_code_filter(instructions_code)

            instructions = instructions_search.get_sobject()

            instructions_text = instructions.get('instructions_text')
        else:
            instructions_text = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions_text))

        return div_wdg
