from tactic.ui.input import TextInputWdg
from tactic.ui.widget import ButtonNewWdg
from tactic.ui.common import BaseTableElementWdg

from pyasm.search import Search
from pyasm.web import SpanWdg, Table


def get_add_audio_configuration_line_behavior(code):
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
function getTableRowsWithAttribute(attribute)
{
  var matchingElements = [];
  var allElements = document.getElementsByTagName('tr');
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
    var audio_config_rows = getTableRowsWithAttribute('code');

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

    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(audio_table, 'qc_reports.AudioLinesTableWdg', {'element_evaluation_code': element_evaluation_code});
    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
        ''' % code
    }

    return behavior


def get_remove_audio_configuration_line_behavior():
    """
    :return: Javascript behavior
    """
    # TODO: Better docstring here

    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''
function getTableRowsWithAttribute(attribute)
{
  var matchingElements = [];
  var allElements = document.getElementsByTagName('tr');
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
    var audio_config_rows = getTableRowsWithAttribute('code');

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

    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(audio_table, 'qc_reports.AudioLinesTableWdg', {'element_evaluation_code': element_evaluation_code});
    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
'''
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

    def get_remove_row_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        remove_row_button = ButtonNewWdg(title='Remove Row', icon='REMOVE')
        remove_row_button.add_class('remove_row_button')
        remove_row_button.add_behavior(get_remove_audio_configuration_line_behavior())

        section_span.add(remove_row_button)

        return section_span

    def get_display(self):
        audio_configuration_table = Table()
        audio_configuration_table.set_id('audio_configuration_table')

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
                self.get_remove_row_button()
            )

        audio_configuration_table.add(self.get_add_row_button())

        return audio_configuration_table
