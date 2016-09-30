from tactic.ui.common import BaseTableElementWdg

from tactic.ui.widget import ButtonNewWdg


class OrderBuilderLauncherWdg(BaseTableElementWdg):
    """
    A widget used to launch the OrderBuilderWdg. Placed in the order table.
    """

    @staticmethod
    def get_launch_behavior(order_search_key):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
try {
    var order_search_key = '%s';

    spt.tab.add_new('order_' + order_search_key, 'Order Builder', 'order_builder.OrderBuilderWdg',
                    {'search_key': order_search_key});
}
catch(err){
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % order_search_key
                    }
        return behavior

    def get_display(self):
        order = self.get_current_sobject()

        order_builder_button = ButtonNewWdg(title='Order Builder for {0}'.format(order.get_code()), icon='WORK')
        order_builder_button.add_behavior(self.get_launch_behavior(order.get_search_key()))

        return order_builder_button
