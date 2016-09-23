from pyasm.widget import SelectWdg
from pyasm.web import Table
from pyasm.widget import CheckboxWdg


def get_file_select_wdg_from_file_list(files, width=400):
    """
    Given a list of file sobjects, return a SelectWdg using the file paths and codes

    :param files: List of file sobjects
    :param width: Width of the SelectWdg
    :return: SelectWdg
    """
    file_select_wdg = SelectWdg('file_select')
    file_select_wdg.set_id('file_select')
    file_select_wdg.add_style('width', '{0}px'.format(width))
    file_select_wdg.add_empty_option()

    for file_sobject in files:
        file_select_wdg.append_option(file_sobject.get('file_path'), file_sobject.get_code())

    return file_select_wdg


def get_files_checkbox_from_file_list(file_sobjects, selected_file_sobjects):
    """
    Given a list of file sobjects, return a table of Checkbox widgets (CheckboxWdg) using the file paths and codes.
    If a file is also in the selected_file_sobjects list, check it automatically.

    :param file_sobjects: List of file sobjects
    :param selected_file_sobjects: List of file sobjects (that are already selected)
    :return: Table
    """

    files_checkbox_table = Table()

    header_row = files_checkbox_table.add_row()
    header = files_checkbox_table.add_header(data='Files', row=header_row)
    header.add_style('text-align', 'center')
    header.add_style('text-decoration', 'underline')

    for file_sobject in file_sobjects:
        checkbox = CheckboxWdg(name=file_sobject.get_code())

        if file_sobject.get_code() in [selected_file.get_code() for selected_file in selected_file_sobjects]:
            checkbox.set_checked()

        checkbox_row = files_checkbox_table.add_row()

        files_checkbox_table.add_cell(data=checkbox, row=checkbox_row)
        files_checkbox_table.add_cell(data=file_sobject.get_value('file_path'), row=checkbox_row)

    return files_checkbox_table
