from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextInputWdg

from pyasm.web import DivWdg, HtmlElement
from pyasm.widget import SubmitWdg

from order_builder_utils import get_select_widget_from_search_type


class NewOrderEntryWdg(BaseRefreshWdg):
    """
    A widget to input an order
    """

    def get_display(self):
        # Set up the outer <div> to hold all the form elements
        outer_div = DivWdg()
        outer_div.add_class('new-order-entry-form')
        outer_div.set_id('new-order-entry-form')

        # Set up the <input> widget for 'name'
        outer_div.add(HtmlElement.label('Name'))
        name_input = TextInputWdg(name='name')
        outer_div.add(name_input)

        # Set up the <input> widget for 'po_number'
        outer_div.add(HtmlElement.label('PO Number'))
        po_number_input = TextInputWdg()
        po_number_input.set_name('po_number')
        outer_div.add(po_number_input)

        # Set up the <select> widget and it's options for 'client'
        outer_div.add(HtmlElement.label('Client'))
        client_select_wdg = get_select_widget_from_search_type('twog/client', 'client', 'name', 'code')
        outer_div.add(client_select_wdg)

        # Set up the Save button
        save_button = SubmitWdg('Save')
        save_button.add_behavior(self.save_button_behavior())
        outer_div.add(save_button)

        # Set up the Save and Add button
        save_and_add_button = SubmitWdg('Save and Add')
        save_and_add_button.add_behavior(self.save_and_add_button_behavior())
        outer_div.add(save_and_add_button)

        return outer_div

    @staticmethod
    def save_button_behavior():
        """
        Save the current order and load the Order Builder widget

        :return: behavior dictionary
        """

        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    function submit_form() {
        spt.api.app_busy_show('Saving...');

        var client_code = values.client;

        // Set up the object for the new title. Note that 'master_title' is always set to true.
        var new_order = {
            'name': values.name,
            'po_number': values.po_number,
            'client_code': client_code
        }

        var server = TacticServerStub.get();

        var inserted_order = server.insert('twog/order', new_order);

        spt.api.app_busy_hide();

        // Load the Order Builder module
        var entry_form = spt.api.get_parent(bvr.src_el, '.new-order-entry-form');
        spt.api.load_panel(entry_form, 'order_builder.OrderBuilderWdg', {'code': inserted_order.get('code')});
    }

    // Get the form values
    var outer_div = spt.api.get_parent(bvr.src_el, '.new-order-entry-form');
    var values = spt.api.get_input_values(outer_div);

    if (!values.client || values.client == '') {
        spt.api.app_busy_hide();
        spt.alert("Please select a client.");
        return;
    }

    submit_form(values);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
        }

        return behavior

    @staticmethod
    def save_and_add_button_behavior():
        """
        Save the current order and reload this widget (to add another order)

        :return: behavior dictionary
        """
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    function submit_form() {
        spt.api.app_busy_show('Saving...');

        var client_code = values.client;

        // Set up the object for the new title. Note that 'master_title' is always set to true.
        var new_order = {
            'name': values.name,
            'po_number': values.po_number,
            'client_code': client_code
        }

        var server = TacticServerStub.get();

        server.insert('twog/order', new_order);

        spt.api.app_busy_hide();

        // Reload the Order Entry widget
        spt.info("The order was entered successfully.");
        var entry_form = spt.api.get_parent(bvr.src_el, '.new-order-entry-form');
        spt.api.load_panel(entry_form, 'order_builder.NewOrderEntryWdg');
    }

    // Get the form values
    var outer_div = spt.api.get_parent(bvr.src_el, '.new-order-entry-form');
    var values = spt.api.get_input_values(outer_div);

    if (!values.client || values.client == '') {
        spt.api.app_busy_hide();
        spt.alert("Please select a client.");
        return;
    }

    submit_form(values);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}'''
        }

        return behavior
