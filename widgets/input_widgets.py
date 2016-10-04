from pyasm.biz import Pipeline
from pyasm.web import Table
from pyasm.widget import CheckboxWdg, SelectWdg, MultiSelectWdg

from common_tools.utils import get_files_for_order, get_files_for_division
from tactic.ui.input import TextInputWdg


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


def get_file_multi_select_wdg_from_file_list(files, width=400):
    """
    Given a list of file sobjects, return a MultiSelectWdg using the file paths and codes

    :param files: List of file sobjects
    :param width: Width of the SelectWdg
    :return: SelectWdg
    """

    file_select_wdg = MultiSelectWdg('file_multi_select')
    file_select_wdg.set_id('file_multi_select')
    file_select_wdg.add_style('width', '{0}px'.format(width))

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


def get_files_checkboxes_for_division(division_code, order_code):
    """
    Given a division code and order code, get a list of Checkbox widgets of the source files associated with a
    division. If the file is already selected in the order, check the checkbox automatically.

    :param division_code: twog/division code
    :param order_code: twog/order code
    :return: Table (of CheckboxWdg)
    """

    files_in_order = get_files_for_order(order_code)
    files_in_division = get_files_for_division(division_code)

    return get_files_checkbox_from_file_list(files_in_division, files_in_order)


def get_file_classification_select_wdg(width=200):
    """
    Get a SelectWdg with the three options available for a file's classification (source, intermediate, and
    deliverable).

    :param width: Width of the widget in pixels (optional)
    :return: SelectWdg
    """
    classification_select_wdg = SelectWdg('file_classification_select')
    classification_select_wdg.set_id('file_classification_select')
    classification_select_wdg.add_style('width', '{0}px'.format(width))

    classification_select_wdg.append_option('Source', 'source')
    classification_select_wdg.append_option('Intermediate', 'intermediate')
    classification_select_wdg.append_option('Deliverable', 'deliverable')

    return classification_select_wdg


def get_text_input_wdg(name, width=200):
    textbox_wdg = TextInputWdg()
    textbox_wdg.set_id(name)
    textbox_wdg.set_name(name)
    textbox_wdg.add_style('width', '{0}px'.format(width))

    return textbox_wdg


def get_task_status_select_wdg(task_sobject):
    """
    Given a sthpw/task sobject, return a SelectWdg with all its potential status options. This is done by looking up
    what those options are through the parent Pipeline.

    :param task_sobject: sthpw/task sobject
    :return: SelectWdg
    """

    task_status_select = SelectWdg('task_status_select')
    task_status_select.set_id('task_status_select')
    task_status_select.add_style('width: 165px;')
    task_status_select.add_empty_option()

    task_pipe_code = task_sobject.get_value('pipeline_code')

    # if the current task has no pipeline, then search for
    # any task pipeline
    if not task_pipe_code:
        # just use the default
        task_pipe_code = 'task'

    pipeline = Pipeline.get_by_code(task_pipe_code)
    if not pipeline:
        pipeline = Pipeline.get_by_code('task')

    for status in pipeline.get_process_names():
        task_status_select.append_option(status, status)

    if task_sobject.get('status'):
        task_status_select.set_value(task_sobject.get('status'))

    return task_status_select
