from tactic.ui.input import TextInputWdg


def get_attribute_or_none(object_with_attribute, attribute):
    """
    Given an object and an attribute that an object is expected to have, return either the object's attribute value, or
    None. The only reason this function exists is because I got tired of typing this line a bunch of times.

    :param object_with_attribute: Object
    :param attribute: Attribute on an object (instance variable)
    :return: Attribute's value or None
    """

    return getattr(object_with_attribute, attribute, None)


def get_text_input_wdg(name, data, width=200, timecode=False):
    textbox_wdg = TextInputWdg()
    textbox_wdg.set_id(name)
    textbox_wdg.set_name(name)
    textbox_wdg.add_style('width', '{0}px'.format(width))

    if timecode:
        textbox_wdg.add_behavior(get_add_colons_for_time_behavior())

    if data:
        textbox_wdg.set_value(data)

    return textbox_wdg


def get_add_colons_for_time_behavior():
    """
    A JavaScript behavior that adds colons in a text box for every two numbers, which makes the input look like a
    timecode.

    :return: JavaScript behavior
    """
    behavior = {'css_class': 'clickme', 'type': 'keyup', 'cbjs_action': '''
try {
    var entered = bvr.src_el.value;
    var new_str = '';
    entered = entered.replace(/:/g,'');
    for(var r = 0; r < entered.length; r++) {
        if(r % 2 == 0 && r != 0) {
            new_str = new_str + ':';
        }
        new_str = new_str + entered[r];
    }
    bvr.src_el.value = new_str;
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
'''}

    return behavior
