from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import ButtonNewWdg

from pyasm.web import DivWdg, HtmlElement

import order_builder.order_builder_utils as obu

from common_tools.utils import get_file_in_package_sobjects_by_package_code,\
    get_file_sobjects_from_file_in_package_sobjects


class PackageInspectWdg(BaseRefreshWdg):
    def init(self):
        self.package_sobject = self.get_sobject_from_kwargs()

    def get_files_list(self):
        outer_div = DivWdg()

        file_in_package_sobjects = get_file_in_package_sobjects_by_package_code(self.package_sobject.get_code())
        file_sobjects = get_file_sobjects_from_file_in_package_sobjects(file_in_package_sobjects)

        files_unordered_html_list = HtmlElement.ul()

        for file_sobject, file_in_package_sobject in zip(file_sobjects, file_in_package_sobjects):
            task_sobject = file_in_package_sobject.get_all_children('sthpw/task')[0]

            file_li = HtmlElement.li()
            file_li.add(file_sobject.get('file_path') + ' - ' + task_sobject.get('status'))

            change_status_button = ButtonNewWdg(title='Change Status')
            change_status_button.add_behavior(
                obu.get_load_popup_widget_with_reload_behavior(
                    'Change Status', 'widgets.ChangeStatusWdg', task_sobject.get_search_key(),
                    'Package', 'widgets.PackageInspectWdg', self.package_sobject.get_search_key()
                )
            )
            change_status_button.add_style('display', 'inline-block')

            file_li.add(change_status_button)

            files_unordered_html_list.add(file_li)

        outer_div.add(files_unordered_html_list)

        return outer_div

    def get_buttons_row(self):
        outer_div = DivWdg()

        note_button = ButtonNewWdg(title='Add Note', icon='NOTE')
        note_button.add_behavior(obu.get_add_notes_behavior(self.package_sobject.get_search_key()))
        note_button.add_style('display', 'inline-block')

        outer_div.add(note_button)

        return outer_div

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('package_inspect_{0}'.format(self.package_sobject.get_code()))

        task_sobject = self.package_sobject.get_all_children('sthpw/task')[0]

        change_status_button = ButtonNewWdg(title='Change Status')
        change_status_button.add_behavior(
            obu.get_load_popup_widget_with_reload_behavior(
                'Change Status', 'widgets.ChangeStatusWdg', task_sobject.get_search_key(),
                'Package', 'widgets.PackageInspectWdg', self.package_sobject.get_search_key()
            )
        )
        change_status_button.add_style('display', 'inline-block')

        outer_div.add(HtmlElement.h4('Status: {0}'.format(task_sobject.get('status'))))
        outer_div.add(change_status_button)

        outer_div.add(HtmlElement.h4('<u>Files</u>'))
        outer_div.add(self.get_files_list())

        outer_div.add(self.get_buttons_row())

        return outer_div
