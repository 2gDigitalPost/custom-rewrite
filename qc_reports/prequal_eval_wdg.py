from pyasm.search import Search
from pyasm.web import DivWdg, SpanWdg, Table
from pyasm.widget import SelectWdg, TextAreaWdg

from tactic.ui.common import BaseRefreshWdg
from tactic.ui.input import TextInputWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg

from qc_reports.prequal_eval_lines_wdg import PrequalEvalLinesWdg


class PrequalEvalWdg(BaseRefreshWdg):

    def init(self):
        self.prequal_eval_sobject = self.get_sobject_from_kwargs()

    @staticmethod
    def get_save_behavior(sobject_code):
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

function save_prequal_eval_lines() {
    var prequal_eval_lines_table = document.getElementById('prequal_eval_lines_table');
    var prequal_eval_rows = getTableRowsWithAttribute(prequal_eval_lines_table, 'code');

    var server = TacticServerStub.get();

    var lines = {};

    for (var i = 0; i < prequal_eval_rows.length; i++) {
        var line_data = {};

        line_data['timecode'] = document.getElementsByName("timecode-" + String(i))[0].value;
        line_data['field'] = document.getElementsByName("field-" + String(i))[0].value;
        line_data['prequal_line_description_code'] = document.getElementsByName("prequal-line-description-" + String(i))[0].value;
        line_data['type_code'] = document.getElementById("type-code-" + String(i)).value;
        line_data['scale'] = document.getElementById("scale-" + String(i)).value;
        line_data['sector_or_channel'] = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        line_data['in_source'] = document.getElementById("in-source-" + String(i)).value;

        var line_search_key = server.build_search_key('twog/prequal_evaluation_line',
                                                      prequal_eval_rows[i].getAttribute('code'), 'twog');

        lines[line_search_key] = line_data;
    }

    server.update_multiple(lines);
}

try {
    var code = '%s';

    save_prequal_eval_lines();

    var server = TacticServerStub.get();
    var search_key = server.build_search_key('twog/prequal_evaluation', code, 'twog');

    // Name of the report
    var name = document.getElementsByName("name_data")[0].value;

    // Client row values
    var client_code = document.getElementById("client_code").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine_code = document.getElementById("machine_code").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate_code = document.getElementById("frame_rate_code").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
        'version': version,
        'po_number': po_number,
        'video_aspect_ratio': video_aspect_ratio,
        'general_comments': general_comments
    };

    var prequal_eval_panel = document.getElementById('prequal_eval_panel');

    spt.app_busy.show("Saving...");
    server.update(search_key, qc_report_object);
    spt.api.load_panel(prequal_eval_panel, 'qc_reports.PrequalEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            ''' % sobject_code
        }

        return behavior

    @staticmethod
    def get_save_new_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Name of the report
    var name = document.getElementsByName("name_data")[0].value;

    // Client row values
    var client_code = document.getElementById("client_code").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine_code = document.getElementById("machine_code").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate_code = document.getElementById("frame_rate_code").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
        'version': version,
        'po_number': po_number,
        'video_aspect_ratio': video_aspect_ratio,
        'general_comments': general_comments
    };

    var prequal_eval_panel = document.getElementById('prequal_eval_panel');

    var server = TacticServerStub.get();

    spt.app_busy.show("Saving a new Report...");

    // Save the new PreQual Evaluation, and get the code that it saved as
    var inserted_prequal_evaluation = server.insert('twog/prequal_evaluation', qc_report_object);
    var code = inserted_prequal_evaluation['code'];

    // Finally, get the search key for the new report, and use it to reload the page
    var search_key = server.build_search_key('twog/prequal_evaluation', code, 'twog');

    spt.api.load_panel(prequal_eval_panel, 'qc_reports.PrequalEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            '''
        }

        return behavior

    @staticmethod
    def get_save_as_new_behavior():
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
    // Name of the report
    var name = document.getElementsByName("name_data")[0].value;

    // Client row values
    var client_code = document.getElementById("client_code").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine_code = document.getElementById("machine_code").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate_code = document.getElementById("frame_rate_code").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    var qc_report_object = {
        'name': name,
        'client_code': client_code,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine_code': machine_code,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate_code': frame_rate_code,
        'version': version,
        'po_number': po_number,
        'video_aspect_ratio': video_aspect_ratio,
        'general_comments': general_comments
    };

    var prequal_eval_panel = document.getElementById('prequal_eval_panel');

    spt.app_busy.show("Saving a new Report...");

    // Save the new Element Evaluation, and get the code that it saved as
    var inserted_prequal_evaluation = server.insert('twog/prequal_evaluation', qc_report_object);
    var code = inserted_prequal_evaluation['code'];

    // Using the code gained from the new report, save the prequal evaluation lines
    var prequal_eval_lines_table = document.getElementById('prequal_eval_lines_table');
    var table_rows = getTableRowsWithAttribute(prequal_eval_lines_table, 'code');

    var server = TacticServerStub.get();

    var lines = {};

    for (var i = 0; i < table_rows.length; i++) {
        var line_data = {};

        line_data['timecode'] = document.getElementsByName("timecode-" + String(i))[0].value;
        line_data['field'] = document.getElementsByName("field-" + String(i))[0].value;
        line_data['prequal_line_description_code'] = document.getElementsByName("prequal-line-description-" + String(i))[0].value;
        line_data['type_code'] = document.getElementById("type-code-" + String(i)).value;
        line_data['scale'] = document.getElementById("scale-" + String(i)).value;
        line_data['sector_or_channel'] = document.getElementsByName("sector-or-channel-" + String(i))[0].value;
        line_data['in_source'] = document.getElementById("in-source-" + String(i)).value;

        var line_search_key = server.build_search_key('twog/prequal_evaluation_line',
                                                      table_rows[i].getAttribute('code'), 'twog');

        lines[line_search_key] = line_data;
    }

    server.update_multiple(lines);

    // Finally, get the search key for the new report, and use it to reload the page
    var search_key = server.build_search_key('twog/prequal_evaluation', code, 'twog');

    spt.api.load_panel(prequal_eval_panel, 'qc_reports.PrequalEvalWdg', {'search_key': search_key});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            '''
        }

        return behavior

    @staticmethod
    def get_export_to_pdf_behavior(sobject_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
var server = TacticServerStub.get();

var code = '%s';
var search_key = server.build_search_key('twog/prequal_evaluation', code, 'twog');

server.execute_cmd('qc_reports.ExportPrequalEvalCommand', {'report_search_key': search_key});
            ''' % sobject_code
        }

        return behavior

    def get_text_input_wdg(self, field_name, width=200):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(field_name)
        textbox_wdg.set_name(field_name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        try:
            textbox_wdg.set_value(self.prequal_eval_sobject.get(field_name))
        except AttributeError:
            pass

        return textbox_wdg

    def get_name_input_wdg(self, width=500):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id('name_data')
        textbox_wdg.set_name('name_data')
        textbox_wdg.add_style('width', '{0}px'.format(width))

        try:
            textbox_wdg.set_value(self.prequal_eval_sobject.get('name'))
        except AttributeError:
            pass

        return textbox_wdg

    def get_name_section(self):
        section_div = DivWdg()

        name_wdg = self.get_name_input_wdg()

        section_div.add('Name: ')
        section_div.add(name_wdg)

        return section_div

    def get_client_section(self):
        section_div = DivWdg()

        client_span = SpanWdg()
        client_span.add_style('display', 'inline-block')
        client_span.add('Client: ')
        client_span.add(self.get_client_select())

        status_span = SpanWdg()
        status_span.add_style('display', 'inline-block')
        status_span.add('Status: ')
        status_span.add(self.get_status_select())

        section_div.add(client_span)
        section_div.add(status_span)

        return section_div

    def get_client_select(self):
        client_sel = SelectWdg('client_select')
        client_sel.set_id('client_code')
        client_sel.add_style('width', '135px')
        client_sel.add_empty_option()

        client_search = Search('twog/client')
        clients = client_search.get_sobjects()

        for client in clients:
            client_sel.append_option(client.get_value('name'), client.get_code())

        try:
            client_sel.set_value(self.prequal_eval_sobject.get('client_code'))
        except AttributeError:
            pass

        return client_sel

    def get_status_select(self):
        status_sel = SelectWdg('status_select')
        status_sel.set_id('status')
        status_sel.add_style('width', '135px')
        status_sel.add_empty_option()

        statuses = ('Approved', 'Condition', 'Rejected')

        for status in statuses:
            status_sel.append_option(status, status)

        if self.prequal_eval_sobject:
            status_sel.set_value(self.prequal_eval_sobject.get_value('status'))

        return status_sel

    def get_operator_section(self):
        operator_table = Table()
        operator_table.add_attr('class', 'operator_table')
        operator_table.add_row()
        operator_table.add_header('DATE')
        operator_table.add_header('OPERATOR')
        operator_table.add_header('STYLE')
        operator_table.add_header('BAY')
        operator_table.add_header('MACHINE')
        operator_table.add_row()

        operator_table.add_cell(self.get_date_calendar_wdg())

        operator_table.add_cell(self.get_text_input_wdg('operator'))

        operator_table.add_cell(self.get_style_select())
        operator_table.add_cell(self.get_bay_select())
        operator_table.add_cell(self.get_machine_select())

        return operator_table

    def get_date_calendar_wdg(self):
        date_calendar_wdg = CalendarInputWdg("date")
        date_calendar_wdg.set_option('show_activator', 'true')
        date_calendar_wdg.set_option('show_time', 'false')
        date_calendar_wdg.set_option('width', '300px')
        date_calendar_wdg.set_option('id', 'date')
        date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        if self.prequal_eval_sobject:
            date_calendar_wdg.set_value(self.prequal_eval_sobject.get_value('date'))

        return date_calendar_wdg

    def get_style_select(self):
        style_sel = SelectWdg('style_select')
        style_sel.set_id('style')
        style_sel.add_style('width: 135px;')
        style_sel.add_empty_option()

        for style in ('Technical', 'Spot QC', 'Mastering'):
            style_sel.append_option(style, style)

        if self.prequal_eval_sobject:
            style_sel.set_value(self.prequal_eval_sobject.get_value('style'))

        return style_sel

    def get_bay_select(self):
        bay_sel = SelectWdg('bay_select')
        bay_sel.set_id('bay')
        bay_sel.add_style('width', '135px')
        bay_sel.add_empty_option()

        for i in range(1, 13):
            bay_sel.append_option('Bay %s' % i, 'Bay %s' % i)

        if self.prequal_eval_sobject:
            bay_sel.set_value(self.prequal_eval_sobject.get_value('bay'))

        return bay_sel

    def get_machine_select(self):
        machine_sel = SelectWdg('machine_select')
        machine_sel.set_id('machine_code')
        machine_sel.add_style('width', '135px')
        machine_sel.add_empty_option()

        machine_search = Search('twog/machine')
        machines = machine_search.get_sobjects()

        for machine in machines:
            machine_sel.append_option(machine.get_value('name'), machine.get_code())

        if self.prequal_eval_sobject:
            machine_sel.set_value(self.prequal_eval_sobject.get_value('machine_code'))

        return machine_sel

    def get_title_section(self):
        section_div = DivWdg()

        section_div.add(self.get_title_input_wdg())
        section_div.add(self.get_format_section())

        return section_div

    def get_title_input_wdg(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('Title: ')

        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id('title_data')
        textbox_wdg.set_name('title_data')
        textbox_wdg.add_style('width', '{0}px'.format(200))

        try:
            textbox_wdg.set_value(self.prequal_eval_sobject.get('title'))
        except AttributeError:
            pass

        section_span.add(textbox_wdg)

        return section_span

    def get_format_section(self):
        section_span = SpanWdg()

        section_span.add('Format: ')
        section_span.add(self.get_format_select_wdg())

        return section_span

    def get_format_select_wdg(self):
        format_sel = SelectWdg('format_select')
        format_sel.set_id('format')
        format_sel.add_style('width', '153px')
        format_sel.add_style('display', 'inline-block')
        format_sel.add_empty_option()

        for file_format in ('Electronic/File', 'File - ProRes', 'File - MXF', 'File - MPEG', 'File - WAV', 'DBC', 'D5',
                            'HDCAM SR', 'NTSC', 'PAL'):
            format_sel.append_option(file_format, file_format)

        if self.prequal_eval_sobject:
            format_sel.set_value(self.prequal_eval_sobject.get_value('format'))

        return format_sel

    def get_season_section(self):
        section_div = DivWdg()

        section_div.add(self.get_season_input_wdg())
        section_div.add(self.get_standard_section())

        return section_div

    def get_season_input_wdg(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('Season: ')

        section_span.add(self.get_text_input_wdg('season', 400))

        return section_span

    def get_standard_section(self):
        section_span = SpanWdg()

        section_span.add('Standard: ')

        standard_select = SelectWdg('standard_select')
        standard_select.set_id('standard')
        standard_select.add_style('width', '153px')
        standard_select.add_style('display', 'inline-block')
        standard_select.add_empty_option()

        for standard in ('625', '525', '720', '1080 (4:4:4)', '1080', 'PAL', 'NTSC'):
            standard_select.append_option(standard, standard)

        if self.prequal_eval_sobject:
            standard_select.set_value(self.prequal_eval_sobject.get_value('standard'))

        section_span.add(standard_select)

        return section_span

    def get_episode_section(self):
        section_div = DivWdg()

        section_div.add(self.get_episode_input_wdg())
        section_div.add(self.get_frame_rate_section())

        return section_div

    def get_episode_input_wdg(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('Episode: ')
        section_span.add(self.get_text_input_wdg('episode', 400))

        return section_span

    def get_frame_rate_section(self):
        section_span = SpanWdg()

        section_span.add('Frame Rate: ')

        frame_rate_select = SelectWdg('frame_rate_select')
        frame_rate_select.set_id('frame_rate_code')
        frame_rate_select.add_style('width', '153px')
        frame_rate_select.add_style('display', 'inline-block')
        frame_rate_select.add_empty_option()

        frame_rate_search = Search('twog/frame_rate')
        frame_rates = frame_rate_search.get_sobjects()

        for frame_rate in frame_rates:
            frame_rate_select.append_option(frame_rate.get_value('name'), frame_rate.get_code())

        if self.prequal_eval_sobject:
            frame_rate_select.set_value(self.prequal_eval_sobject.get_value('frame_rate_code'))

        section_span.add(frame_rate_select)

        return section_span

    def get_version_section(self):
        section_div = DivWdg()

        section_div.add(self.get_version_input_wdg())
        section_div.add(self.get_po_number_section())

        return section_div

    def get_version_input_wdg(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('Version: ')
        section_span.add(self.get_text_input_wdg('version', 400))

        return section_span

    def get_po_number_section(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('PO #: ')
        section_span.add(self.get_text_input_wdg('po_number', 100))

        return section_span

    def get_video_aspect_ratio_section(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('Video Aspect Ratio: ')
        section_span.add(self.get_video_aspect_ratio_select_wdg())

        return section_span

    def get_video_aspect_ratio_select_wdg(self):
        video_aspect_ratio_sel = SelectWdg('video_aspect_ratio_select')
        video_aspect_ratio_sel.set_id('video_aspect_ratio')
        video_aspect_ratio_sel.add_style('width', '300px')
        video_aspect_ratio_sel.add_style('display', 'inline-block')
        video_aspect_ratio_sel.add_empty_option()

        for video_aspect_ratio in ('16x9 1.33', '16x9 1.33 Pan & Scan', '16x9 1.78 Anamorphic', '16x9 1.78 Full Frame',
                                   '16x9 1.85 Letterbox', '16x9 1.85 Matted', '16x9 1.85 Matted Anamorphic',
                                   '16x9 2.00 Letterbox', '16x9 2.10 Letterbox', '16x9 2.20 Letterbox',
                                   '16x9 2.35 Anamorphic', '16x9 2.35 Letterbox', '16x9 2.40 Letterbox',
                                   '16x9 2.55 Letterbox', '4x3 1.33 Full Frame', '4x3 1.78 Letterbox',
                                   '4x3 1.85 Letterbox',
                                   '4x3 2.35 Letterbox', '4x3 2.40 Letterbox'):
            video_aspect_ratio_sel.append_option(video_aspect_ratio, video_aspect_ratio)

        if self.prequal_eval_sobject:
            video_aspect_ratio_sel.set_value(self.prequal_eval_sobject.get_value('video_aspect_ratio'))

        return video_aspect_ratio_sel

    def get_general_comments_section(self):
        general_comments_div = DivWdg()
        general_comments_div.add_style('margin', '10px')
        general_comments_wdg = TextAreaWdg()
        general_comments_wdg.set_id('general_comments')
        general_comments_wdg.set_input_prefix('test')

        if self.prequal_eval_sobject:
            general_comments_wdg.set_value(self.prequal_eval_sobject.get_value('general_comments'))

        general_comments_text_div = DivWdg('General Comments')
        general_comments_text_div.add_style('font-weight', 'bold')
        general_comments_div.add(general_comments_text_div)
        general_comments_div.add(general_comments_wdg)

        return general_comments_div

    def get_save_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_button = ButtonNewWdg(title='Save', icon='SAVE')
        save_button.add_class('save_button')
        save_button.add_behavior(self.get_save_behavior(self.prequal_eval_sobject.get_code()))

        section_span.add(save_button)

        return section_span

    def get_save_new_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_new_button = ButtonNewWdg(title='Save New Report', icon='NEW')
        save_new_button.add_class('save_new_button')
        save_new_button.add_behavior(self.get_save_new_behavior())

        section_span.add(save_new_button)

        return section_span

    def get_save_as_new_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_as_new_button = ButtonNewWdg(title='Save As', icon='NEW')
        save_as_new_button.add_class('save_as_new_button')
        save_as_new_button.add_behavior(self.get_save_as_new_behavior())

        section_span.add(save_as_new_button)

        return section_span

    def get_export_to_pdf_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_as_new_button = ButtonNewWdg(title='Export to PDF', icon='ARROW_DOWN')
        save_as_new_button.add_class('save_as_new_button')
        save_as_new_button.add_behavior(self.get_export_to_pdf_behavior(self.prequal_eval_sobject.get_code()))

        section_span.add(save_as_new_button)

        return section_span

    def get_display(self):
        main_wdg = DivWdg()
        main_wdg.set_id('prequal_eval_panel')

        main_wdg.add(self.get_name_section())
        main_wdg.add(self.get_client_section())

        main_wdg.add(self.get_operator_section())
        main_wdg.add(self.get_title_section())
        main_wdg.add(self.get_season_section())
        main_wdg.add(self.get_episode_section())
        main_wdg.add(self.get_version_section())
        main_wdg.add(self.get_video_aspect_ratio_section())

        main_wdg.add(self.get_general_comments_section())

        if hasattr(self, 'prequal_eval_sobject') and self.prequal_eval_sobject:
            main_wdg.add(PrequalEvalLinesWdg(prequal_eval_code=self.prequal_eval_sobject.get_code()))
            main_wdg.add(self.get_save_button())
            main_wdg.add(self.get_export_to_pdf_button())
            main_wdg.add(self.get_save_as_new_button())
        else:
            main_wdg.add(self.get_save_new_button())

        return main_wdg
