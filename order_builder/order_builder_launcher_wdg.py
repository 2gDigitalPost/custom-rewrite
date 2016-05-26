from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class OrderBuilderLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the OrderBuilderWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(order_code):
        # TODO: Make this open a new tab rather than reloading the current one
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var order_code = '%s';

    spt.api.load_tab('Order Builder', 'order_builder.OrderBuilderWdg', {'code': order_code});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % order_code
                    }
        return behavior

    def get_display(self):
        order_code = self.get_current_sobject().get_code()

        order_builder_button = ButtonNewWdg(title='Order Builder for {0}'.format(order_code), icon='WORK')
        order_builder_button.add_behavior(self.get_launch_behavior(order_code))

        return order_builder_button
