from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg
from pyasm.widget import SubmitWdg

from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg


class ChangeDueDateWdg(BaseRefreshWdg):
    def init(self):
        self.title_order_code = self.get_kwargs().get('title_order_code')
        self.current_date = self.get_kwargs().get('due_date')

    def get_date_calendar_wdg(self):
        date_calendar_wdg = CalendarInputWdg("date")
        date_calendar_wdg.set_option('show_activator', 'true')
        date_calendar_wdg.set_option('show_time', 'false')
        date_calendar_wdg.set_option('width', '300px')
        date_calendar_wdg.set_option('id', 'date')
        date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        try:
            date_calendar_wdg.set_value(self.current_date)
        except AttributeError:
            pass

        return date_calendar_wdg

    @staticmethod
    def save_button_behavior(title_order_code):
        """
        Save the new date and close the popup

        :return: behavior dictionary
        """

        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
function submit_form() {
    spt.api.app_busy_show('Saving...');

    var server = TacticServerStub.get();
    var date = values.date;
    var title_order_code = '%s';

    var search_key = server.build_search_key('twog/title_order', title_order_code, 'twog');

    server.update(search_key, {'due_date': date});

    spt.api.app_busy_hide();
}

try {
    // Get the form values
    var outer_div = spt.api.get_parent(bvr.src_el, '#change_due_date_wdg');
    var values = spt.api.get_input_values(outer_div, null, false);

    submit_form(values);

    // Close the popup
    spt.popup.close(outer_div);

    spt.panel.refresh()
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % title_order_code
        }

        return behavior

    def get_save_new_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_new_button = ButtonNewWdg(title='Save', icon='NEW')
        save_new_button.add_class('save_due_date')
        save_new_button.add_behavior(self.get_save_new_behavior())

        section_span.add(save_new_button)

        return section_span

    def get_display(self):
        calendar_input = self.get_date_calendar_wdg()

        # Set up the Save button
        save_button = SubmitWdg('Save')
        save_button.add_behavior(self.save_button_behavior(self.title_order_code))

        main_wdg = DivWdg()
        main_wdg.set_id('change_due_date_wdg')

        main_wdg.add(calendar_input)
        main_wdg.add(save_button)

        return main_wdg
