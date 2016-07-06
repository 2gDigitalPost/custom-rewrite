

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
'''
    }

    return behavior