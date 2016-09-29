from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg

from common_tools.utils import get_instructions_text_from_instructions_code


class ComponentInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()

    @staticmethod
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line[0:3] == '###':
                    formatted_line = '<h4>{0}</h4>'.format(line[4:])
                else:
                    formatted_line = '<p>{0}</p>'.format(line)

                output_html += formatted_line

        return output_html

    def get_display(self):
        div_wdg = DivWdg()

        instructions_code = self.component_sobject.get('instructions_code')

        if instructions_code:
            instructions_text = get_instructions_text_from_instructions_code(instructions_code)
        else:
            instructions_text = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions_text.encode('utf-8')))

        return div_wdg
