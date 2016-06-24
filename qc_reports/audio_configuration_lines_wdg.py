from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseTableElementWdg

from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table


def get_add_audio_configuration_line_behavior(element_eval_code):
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
function getTableRowsWithAttribute(table, attribute)
{
  var matchingElements = [];
  var allElements = table.getElementsByTagName('tr');
  for (var i = 0, n = allElements.length; i < n; i++)
  {
    if (allElements[i].getAttribute(attribute) !== null)
    {
      // Element exists with attribute. Add to array.
      matchingElements.push(allElements[i]);
    }
  }
  return matchingElements;
}

try {
    var element_evaluation_code = '%s';

    var audio_table = document.getElementById('audio_configuration_table');
    var audio_config_rows = getTableRowsWithAttribute(audio_table, 'code');

    var server = TacticServerStub.get();

    for (var i = 0; i < audio_config_rows.length; i++) {
        var audio_line = {};

        audio_line['channel'] = document.getElementsByName("channel-" + String(i))[0].value;
        audio_line['content'] = document.getElementsByName("content-" + String(i))[0].value;
        audio_line['tone'] = document.getElementsByName("tone-" + String(i))[0].value;
        audio_line['peak'] = document.getElementsByName("peak-" + String(i))[0].value;

        var search_key = server.build_search_key('twog/audio_evaluation_line',
                                                 audio_config_rows[i].getAttribute('code'), 'twog');

        server.update(search_key, audio_line);
    }

    // Insert a blank line
    server.insert('twog/audio_evaluation_line', {'element_evaluation_code': element_evaluation_code});

    // Refresh the widget
    var audio_div = document.getElementById('audio_config_lines_div');

    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(audio_div, 'qc_reports.AudioLinesTableWdg', {'element_evaluation_code': element_evaluation_code});
    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
        ''' % element_eval_code
    }

    return behavior


def get_remove_audio_configuration_line_behavior(element_eval_code, line_code):
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
try {
    var server = TacticServerStub.get();
    var element_evaluation_code = '%s';
    var line_code = '%s';

    server.retire_sobject(server.build_search_key('twog/audio_evaluation_line', line_code, 'twog'));

    // Refresh the widget
    var audio_div = document.getElementById('audio_config_lines_div');

    spt.api.load_panel(audio_div, 'qc_reports.AudioLinesTableWdg', {'element_evaluation_code': element_evaluation_code});
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
''' % (element_eval_code, line_code)
    }

    return behavior


class AudioLinesTableWdg(BaseTableElementWdg):
    def init(self):
        self.element_evaluation_code = self.kwargs.get('element_evaluation_code')

        if self.element_evaluation_code:
            lines_search = Search('twog/audio_evaluation_line')
            lines_search.add_filter('element_evaluation_code', self.element_evaluation_code)
            self.lines = lines_search.get_sobjects()
        else:
            self.lines = []

    def get_text_input_wdg_for_audio_config(self, name, width=200, line_data=None):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if line_data:
            textbox_wdg.set_value(line_data)

        return textbox_wdg

    def get_add_row_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_behavior(get_add_audio_configuration_line_behavior(self.element_evaluation_code))

        section_span.add(add_row_button)

        return section_span

    def get_remove_row_button(self, line_code):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='REMOVE')
        remove_row_button.add_class('remove_row_button')
        remove_row_button.add_behavior(get_remove_audio_configuration_line_behavior(self.element_evaluation_code,
                                                                                    line_code))

        section_span.add(remove_row_button)

        return section_span

    def get_display(self):
        audio_configuration_table = Table()
        audio_configuration_table.set_id('audio_configuration_table')
        audio_configuration_table.add_style('margin', '10px')

        if self.lines:
            audio_configuration_table.add_row()
            audio_configuration_table.add_header('Audio Configuration')

            audio_configuration_table.add_row()
            audio_configuration_table.add_header('Channel')
            audio_configuration_table.add_header('Content')
            audio_configuration_table.add_header('Tone')
            audio_configuration_table.add_header('Peak')

            for iterator, line in enumerate(self.lines):
                current_row = audio_configuration_table.add_row()

                current_row.add_attr('code', line.get_code())

                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('channel-{0}'.format(iterator), 150, line.get_value('channel'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('content-{0}'.format(iterator), 150, line.get_value('content'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('tone-{0}'.format(iterator), 150, line.get_value('tone'))
                )
                audio_configuration_table.add_cell(
                    self.get_text_input_wdg_for_audio_config('peak-{0}'.format(iterator), 150, line.get_value('peak'))
                )
                audio_configuration_table.add_cell(
                    self.get_remove_row_button(line.get_code())
                )
        else:
            audio_configuration_table.add("No Audio Configuration lines exist yet. Add one?")

        audio_configuration_table.add(self.get_add_row_button())

        main_div = DivWdg()
        main_div.set_id('audio_config_lines_div')
        main_div.add_style('margin', '10px')
        main_div.add(audio_configuration_table)

        return main_div
