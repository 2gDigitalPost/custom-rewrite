from tactic.ui.common import BaseRefreshWdg

from pyasm.web import DivWdg
from pyasm.widget import SubmitWdg

from input_widgets import get_text_input_wdg, get_file_classification_select_wdg


class EditFileWdg(BaseRefreshWdg):
    """
    A quick edit widget to edit one twog/file entry. Displays the file_path as a string input field, and classification
    as a SelectWdg
    """

    def init(self):
        self.file_sobject = self.get_sobject_from_kwargs()
        self.parent_widget_title = self.kwargs.get('parent_widget_title')
        self.parent_widget_name = self.kwargs.get('parent_widget_name')
        self.parent_widget_search_key = self.kwargs.get('parent_widget_search_key')

    def submit_button_behavior(self):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var file_code = '%s';

// Get the server object
var server = TacticServerStub.get();
var containing_element = bvr.src_el.getParent("#edit_file_" + file_code);
var values = spt.api.get_input_values(containing_element, null, false);

var file_path = values["file_path_input"];
var classification = values["file_classification_select"];

var kwargs = {
    'file_path': file_path,
    'classification': classification
}

var file_search_key = server.build_search_key('twog/file', file_code, 'twog');

server.update(file_search_key, kwargs);

spt.app_busy.hide();
spt.popup.close(spt.popup.get_popup(bvr.src_el));

var parent_widget_title = '%s';
var parent_widget_name = '%s';
var parent_widget_search_key = '%s';

spt.api.load_tab(parent_widget_title, parent_widget_name, {'search_key': parent_widget_search_key});
''' % (self.file_sobject.get_code(),  self.parent_widget_title, self.parent_widget_name, self.parent_widget_search_key)
        }

        return behavior

    def get_display(self):
        div_wdg = DivWdg()
        div_wdg.set_id('edit_file_{0}'.format(self.file_sobject.get_code()))

        div_wdg.add(get_text_input_wdg('file_path_input', pretext=self.file_sobject.get('file_path')))
        div_wdg.add(get_file_classification_select_wdg(selected=self.file_sobject.get('classification')))

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.submit_button_behavior())
        submit_button.add_style('display', 'block')

        div_wdg.add(submit_button)

        return div_wdg
