from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.search import Search
from pyasm.web import DivWdg, HtmlElement, SpanWdg

from common_tools.utils import get_department_instructions_sobjects_for_instructions_template_code


class InstructionsTemplateBuilderWdg(BaseRefreshWdg):
    def init(self):
        self.instructions_template_sobject = self.get_sobject_from_kwargs()

    def get_div_for_department_instructions(self, department_instructions_sobject):
        department_instructions_div = DivWdg()

        department_instructions_div.add(HtmlElement.h4(department_instructions_sobject.get('name')))
        department_instructions_div.add(HtmlElement.p(department_instructions_sobject.get('instructions_text')))

        return department_instructions_div

    def get_selected_department_instructions_section(self):
        department_instructions_list = HtmlElement.ul()
        department_instructions_list.add_style('list-style-type', 'none')

        department_instructions_sobjects = get_department_instructions_sobjects_for_instructions_template_code(
            self.instructions_template_sobject.get_code())

        for department_instructions_sobject in department_instructions_sobjects:
            li = HtmlElement.li()
            li.add(self.get_div_for_department_instructions(department_instructions_sobject))
            department_instructions_list.add(li)

        return department_instructions_list

    def get_unselected_department_instructions_section(self):
        department_instructions_list = HtmlElement.ul()
        department_instructions_list.add_style('list-style-type', 'none')

    def get_display(self):
        instructions_template_div = DivWdg()
        instructions_template_div.set_id('instructions_template')
        instructions_template_div.add_style('display', 'inline-block')

        instructions_template_name_div = DivWdg()
        instructions_template_name_div.add_style('text-decoration', 'underline')
        instructions_template_name_div.add_style('font-size', '24px')
        instructions_template_name_div.add(self.instructions_template_sobject.get('name'))

        instructions_template_div.add(instructions_template_name_div)
        instructions_template_div.add(self.get_selected_department_instructions_section())

        department_instructions_div = DivWdg()
        department_instructions_div.set_id('department_instructions')
        department_instructions_div.add_style('display', 'inline-block')

        department_instructions_div.add('Test')

        outer_div = DivWdg()
        outer_div.set_id('instructions_template_builder')
        outer_div.add(instructions_template_div)
        outer_div.add(department_instructions_div)

        return outer_div
