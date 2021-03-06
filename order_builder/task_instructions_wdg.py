from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg

from common_tools.utils import get_task_instructions_text_from_instructions_code


class TaskInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()

    @staticmethod
    def parse_instruction_text(instructions):
        output_html = ''

        for line in instructions.split('\n'):
            if line:
                if line.startswith('!@|'):
                    name = line.split('|')[1].strip()
                    formatted_line = '<h4>{0}</h4>'.format(name)
                else:
                    formatted_line = '<p>{0}</p>'.format(line)

                output_html += formatted_line

        return output_html

    def get_display(self):
        div_wdg = DivWdg()

        parent_component = self.task_sobject.get_parent()
        instructions_code = parent_component.get('instructions_code')
        instructions = get_task_instructions_text_from_instructions_code(instructions_code,
                                                                         self.task_sobject.get('process'))

        if not instructions:
            instructions = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions.encode('utf-8')))

        return div_wdg
