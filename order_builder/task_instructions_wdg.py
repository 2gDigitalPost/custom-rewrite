from pyasm.search import Search
from pyasm.web import DivWdg

from tactic.ui.common import BaseRefreshWdg


class TaskInstructionsWdg(BaseRefreshWdg):
    def init(self):
        self.task_sobject = self.get_sobject_from_kwargs()

    @staticmethod
    def get_instructions_for_task_name(name, instructions):
        instructions_lines = []
        within_instructions = False

        for line in instructions.split('\n'):
            if line.startswith('#'):
                if line == '# {0}'.format(name):
                    within_instructions = True
                else:
                    within_instructions = False

            if within_instructions:
                instructions_lines.append(line)

        return '\n'.join(instructions_lines)

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

    @staticmethod
    def get_title_order_instructions_from_task(task):
        title_order_sobject = task.get_parent()

        instructions_search = Search('twog/instructions')
        instructions_search.add_code_filter(title_order_sobject.get('instructions_code'))
        instructions = instructions_search.get_sobject()

        # return title_order_sobject.get_value('instructions')
        return instructions.get('instructions_text')

    def get_display(self):
        div_wdg = DivWdg()

        instructions = self.get_instructions_for_task_name(self.task_sobject.get_value('process'),
                                                           self.get_title_order_instructions_from_task(
                                                               self.task_sobject
                                                           ))

        if not instructions:
            instructions = 'Sorry, instructions have not been added yet.'

        div_wdg.add(self.parse_instruction_text(instructions))

        return div_wdg
