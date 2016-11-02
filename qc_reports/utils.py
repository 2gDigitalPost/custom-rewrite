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


def calculate_duration(timecode_in, timecode_out, frame_rate):
    """
    Given two time codes (one in, one out) and a frame rate, calculate the difference between the two time codes,
    returning in the format HOURS:MINUTES:SECONDS:FRAMES

    Calculation is done by first converting the time codes to seconds, then to frames based on the frame rate. Subtract
    the in time code from the out time code, convert back to the original format, and return the result.

    Note that if the timecode_in is greater than the timecode_out, the calculation won't fail, but will return some
    strange results. It is the operator's responsibility to fix the time codes in this scenario.

    :param timecode_in: String (format: HH:MM:SS:FF)
    :param timecode_out: String (format: HH:MM:SS:FF) (should be greater than timecode_in)
    :param frame_rate: Int
    :return: String (format: HH:MM:SS:FF)
    """
    hours_in, minutes_in, seconds_in, frames_in = timecode_in.split(':')
    hours_out, minutes_out, seconds_out, frames_out = timecode_out.split(':')

    frames_in = int(frames_in)
    frames_out = int(frames_out)
    seconds_in = int(seconds_in)
    seconds_out = int(seconds_out)

    seconds_in += int(hours_in) * 60 * 60
    seconds_in += int(minutes_in) * 60

    seconds_out += int(hours_out) * 60 * 60
    seconds_out += int(minutes_out) * 60

    frames_in += seconds_in * frame_rate
    frames_out += seconds_out * frame_rate

    duration_in_frames = frames_out - frames_in

    seconds, frames = divmod(duration_in_frames, frame_rate)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    duration_string = '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(hours, minutes, seconds, frames)

    return duration_string


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
