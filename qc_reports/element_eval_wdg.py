from qc_reports.audio_configuration_lines_wdg import AudioLinesTableWdg
from qc_reports.element_eval_lines_wdg import ElementEvalLinesWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.input import TextInputWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg

from pyasm.search import Search
from pyasm.web import Table, DivWdg, SpanWdg
from pyasm.widget import SelectWdg, CheckboxWdg, TextAreaWdg


def get_image_div():
    image_cell = '<img src="/reports/2GLogo_small4.png"/>'
    image_div = DivWdg()
    image_div.add(image_cell)
    image_div.add_style('float', 'left')
    image_div.add_style('margin', '5px')

    return image_div


def get_address_div():
    address_div = DivWdg()

    address_name_div = DivWdg('2G Digital Post, Inc.')
    address_name_div.add_style('font-weight', 'bold')

    address_street_div = DivWdg('280 E. Magnolia Blvd.')
    address_city_div = DivWdg('Burbank, CA 91502')
    address_phone_div = DivWdg('310-840-0600')
    address_url_div = DivWdg('www.2gdigitalpost.com')

    [address_div.add(div) for div in [address_name_div, address_street_div, address_city_div, address_phone_div,
                                      address_url_div]]
    address_div.add_style('display', 'inline-block')

    return address_div


def get_client_name(client_name):
    client_name_div = DivWdg(client_name)
    client_name_div.add_style('font-size', '40px')
    client_name_div.add_style('display', 'inline-block')
    client_name_div.add_style('padding', '10px')

    return client_name_div


def get_approved_rejected_checkboxes(conclusion):
    acr_s = ['APPROVED', 'REJECTED']
    acr = Table()
    acr.add_style('display', 'inline-block')

    for mark in acr_s:
        acr.add_row()
        acr1 = CheckboxWdg('marked_%s' % mark)

        if mark in conclusion:
            acr1.set_value(True)
        else:
            acr1.set_value(False)

        acr.add_cell(acr1)
        acr.add_cell('<b>{0}</b>'.format(mark))

    return acr


class ElementEvalWdg(BaseTableElementWdg):

    def init(self):
        self.element_eval_sobject = self.get_sobject_from_kwargs()

        if self.element_eval_sobject:
            self.name = self.element_eval_sobject.get('name')
            self.title_data = self.element_eval_sobject.get('title') # self.title is already used in the super class
            self.client = self.element_eval_sobject.get('client')
            self.status = self.element_eval_sobject.get('status')
            self.date = self.element_eval_sobject.get('date')
            self.operator = self.element_eval_sobject.get('operator')
            self.style_sel = self.element_eval_sobject.get('style') # self.style is already used in the super class
            self.bay = self.element_eval_sobject.get('bay')
            self.machine = self.element_eval_sobject.get('machine')
            self.format_data = self.element_eval_sobject.get('format') # 'format' is a reserved word in Python
            self.season = self.element_eval_sobject.get('season')
            self.standard = self.element_eval_sobject.get('standard')
            self.episode = self.element_eval_sobject.get('episode')
            self.frame_rate = self.element_eval_sobject.get('frame_rate')
            self.version = self.element_eval_sobject.get('version')
            self.po_number = self.element_eval_sobject.get('po_number')
            self.file_name = self.element_eval_sobject.get('file_name')
            self.roll_up_blank = self.element_eval_sobject.get('roll_up_blank')
            self.bars_tone = self.element_eval_sobject.get('bars_tone')
            self.black_silence_1 = self.element_eval_sobject.get('black_silence_1')
            self.slate_silence = self.element_eval_sobject.get('slate_silence')
            self.black_silence_2 = self.element_eval_sobject.get('black_silence_2')
            self.start_of_program = self.element_eval_sobject.get('start_of_program')
            self.end_of_program = self.element_eval_sobject.get('end_of_program')
            self.active_video_begins = self.element_eval_sobject.get('active_video_begins')
            self.active_video_ends = self.element_eval_sobject.get('active_video_ends')
            self.horizontal_blanking = self.element_eval_sobject.get('horizontal_blanking')
            self.luminance_peak = self.element_eval_sobject.get('luminance_peak')
            self.chroma_peak = self.element_eval_sobject.get('chroma_peak')
            self.head_logo = self.element_eval_sobject.get('head_logo')
            self.tail_logo = self.element_eval_sobject.get('tail_logo')
            self.total_runtime = self.element_eval_sobject.get('total_runtime')
            self.language = self.element_eval_sobject.get('language')
            self.tv_feature_trailer = self.element_eval_sobject.get('tv_feature_trailer')
            self.cc_subtitles = self.element_eval_sobject.get('cc_subtitles')
            self.video_aspect_ratio = self.element_eval_sobject.get('video_aspect_ratio')
            self.vitc = self.element_eval_sobject.get('vitc')
            self.textless_tail = self.element_eval_sobject.get('textless_tail')
            self.source_barcode = self.element_eval_sobject.get('source_barcode')
            self.notices = self.element_eval_sobject.get('notices')
            self.element_qc_barcode = self.element_eval_sobject.get('element_qc_barcode')
            self.label = self.element_eval_sobject.get('label')
            self.record_date = self.element_eval_sobject.get('record_date')
            self.general_comments = self.element_eval_sobject.get('general_comments')

    @staticmethod
    def get_save_behavior(sobject_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    var code = '%s';

    var server = TacticServerStub.get();
    var search_key = server.build_search_key('twog/element_evaluation', code, 'twog');

    // Name of the report
    var name = document.getElementsByName("name")[0].value;

    // Client row values
    var client = document.getElementById("client").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine = document.getElementById("machine").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate = document.getElementById("frame_rate").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var file_name = document.getElementsByName("file_name")[0].value;

    // Program Format values
    var roll_up_blank = document.getElementsByName("roll_up_blank")[0].value;
    var bars_tone = document.getElementsByName("bars_tone")[0].value;
    var black_silence_1 = document.getElementsByName("black_silence_1")[0].value;
    var slate_silence = document.getElementsByName("slate_silence")[0].value;
    var black_silence_2 = document.getElementsByName("black_silence_2")[0].value;
    var start_of_program = document.getElementsByName("start_of_program")[0].value;
    var end_of_program = document.getElementsByName("end_of_program")[0].value;

    // Video Measurements values
    var active_video_begins = document.getElementsByName("active_video_begins")[0].value;
    var active_video_ends = document.getElementsByName("active_video_ends")[0].value;
    var horizontal_blanking = document.getElementsByName("horizontal_blanking")[0].value;
    var luminance_peak = document.getElementsByName("luminance_peak")[0].value;
    var chroma_peak = document.getElementsByName("chroma_peak")[0].value;
    var head_logo = document.getElementsByName("head_logo")[0].value;
    var tail_logo = document.getElementsByName("tail_logo")[0].value;

    // Element Profile values
    var total_runtime = document.getElementsByName("total_runtime")[0].value;
    var language = document.getElementsByName("language")[0].value;
    var tv_feature_trailer = document.getElementsByName("tv_feature_trailer")[0].value;
    var cc_subtitles = document.getElementsByName("cc_subtitles")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;
    var vitc = document.getElementsByName("vitc")[0].value;
    var textless_tail = document.getElementsByName("textless_tail")[0].value;
    var source_barcode = document.getElementsByName("source_barcode")[0].value;
    var notices = document.getElementsByName("notices")[0].value;
    var element_qc_barcode = document.getElementsByName("element_qc_barcode")[0].value;
    var label = document.getElementById("label").value;
    var record_date = document.getElementsByName("record_date")[0].value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    var qc_report_object = {
        'name': name,
        'client': client,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine': machine,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate': frame_rate,
        'version': version,
        'po_number': po_number,
        'file_name': file_name,
        'roll_up_blank': roll_up_blank,
        'bars_tone': bars_tone,
        'black_silence_1': black_silence_1,
        'slate_silence': slate_silence,
        'black_silence_2': black_silence_2,
        'start_of_program': start_of_program,
        'end_of_program': end_of_program,
        'active_video_begins': active_video_begins,
        'active_video_ends': active_video_ends,
        'horizontal_blanking': horizontal_blanking,
        'luminance_peak': luminance_peak,
        'chroma_peak': chroma_peak,
        'head_logo': head_logo,
        'tail_logo': tail_logo,
        'total_runtime': total_runtime,
        'language': language,
        'tv_feature_trailer': tv_feature_trailer,
        'cc_subtitles': cc_subtitles,
        'video_aspect_ratio': video_aspect_ratio,
        'vitc': vitc,
        'textless_tail': textless_tail,
        'source_barcode': source_barcode,
        'notices': notices,
        'element_qc_barcode': element_qc_barcode,
        'label': label,
        'record_date': record_date,
        'general_comments': general_comments
    };

    var element_eval_panel = document.getElementById('element_eval_panel');

    spt.app_busy.show("Saving...");
    server.update(search_key, qc_report_object);
    spt.api.load_panel(element_eval_panel, 'qc_reports.ElementEvalWdg', {'search_key': search_key});

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
    def get_save_as_new_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Name of the report
    var name = document.getElementsByName("name")[0].value;

    // Client row values
    var client = document.getElementById("client").value;
    var status = document.getElementById("status").value;

    // Operator row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine = document.getElementById("machine").value;

    // Title section values
    var title_data = document.getElementsByName("title_data")[0].value;
    var format = document.getElementById("format").value;
    var season = document.getElementsByName("season")[0].value;
    var standard = document.getElementById("standard").value;
    var episode = document.getElementsByName("episode")[0].value;
    var frame_rate = document.getElementById("frame_rate").value;
    var version = document.getElementsByName("version")[0].value;
    var po_number = document.getElementsByName("po_number")[0].value;
    var file_name = document.getElementsByName("file_name")[0].value;

    // Program Format values
    var roll_up_blank = document.getElementsByName("roll_up_blank")[0].value;
    var bars_tone = document.getElementsByName("bars_tone")[0].value;
    var black_silence_1 = document.getElementsByName("black_silence_1")[0].value;
    var slate_silence = document.getElementsByName("slate_silence")[0].value;
    var black_silence_2 = document.getElementsByName("black_silence_2")[0].value;
    var start_of_program = document.getElementsByName("start_of_program")[0].value;
    var end_of_program = document.getElementsByName("end_of_program")[0].value;

    // Video Measurements values
    var active_video_begins = document.getElementsByName("active_video_begins")[0].value;
    var active_video_ends = document.getElementsByName("active_video_ends")[0].value;
    var horizontal_blanking = document.getElementsByName("horizontal_blanking")[0].value;
    var luminance_peak = document.getElementsByName("luminance_peak")[0].value;
    var chroma_peak = document.getElementsByName("chroma_peak")[0].value;
    var head_logo = document.getElementsByName("head_logo")[0].value;
    var tail_logo = document.getElementsByName("tail_logo")[0].value;

    // Element Profile values
    var total_runtime = document.getElementsByName("total_runtime")[0].value;
    var language = document.getElementsByName("language")[0].value;
    var tv_feature_trailer = document.getElementsByName("tv_feature_trailer")[0].value;
    var cc_subtitles = document.getElementsByName("cc_subtitles")[0].value;
    var video_aspect_ratio = document.getElementById("video_aspect_ratio").value;
    var vitc = document.getElementsByName("vitc")[0].value;
    var textless_tail = document.getElementsByName("textless_tail")[0].value;
    var source_barcode = document.getElementsByName("source_barcode")[0].value;
    var notices = document.getElementsByName("notices")[0].value;
    var element_qc_barcode = document.getElementsByName("element_qc_barcode")[0].value;
    var label = document.getElementById("label").value;
    var record_date = document.getElementsByName("record_date")[0].value;

    // General comments
    var general_comments = document.getElementById("general_comments").value;

    var qc_report_object = {
        'name': name,
        'client': client,
        'status': status,
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine': machine,
        'title': title_data,
        'format': format,
        'season': season,
        'standard': standard,
        'episode': episode,
        'frame_rate': frame_rate,
        'version': version,
        'po_number': po_number,
        'file_name': file_name,
        'roll_up_blank': roll_up_blank,
        'bars_tone': bars_tone,
        'black_silence_1': black_silence_1,
        'slate_silence': slate_silence,
        'black_silence_2': black_silence_2,
        'start_of_program': start_of_program,
        'end_of_program': end_of_program,
        'active_video_begins': active_video_begins,
        'active_video_ends': active_video_ends,
        'horizontal_blanking': horizontal_blanking,
        'luminance_peak': luminance_peak,
        'chroma_peak': chroma_peak,
        'head_logo': head_logo,
        'tail_logo': tail_logo,
        'total_runtime': total_runtime,
        'language': language,
        'tv_feature_trailer': tv_feature_trailer,
        'cc_subtitles': cc_subtitles,
        'video_aspect_ratio': video_aspect_ratio,
        'vitc': vitc,
        'textless_tail': textless_tail,
        'source_barcode': source_barcode,
        'notices': notices,
        'element_qc_barcode': element_qc_barcode,
        'label': label,
        'record_date': record_date,
        'general_comments': general_comments
    };

    var element_eval_panel = document.getElementById('element_eval_panel');

    var server = TacticServerStub.get();

    spt.app_busy.show("Saving a new Report...");
    var inserted_sobject = server.insert('twog/element_evaluation', qc_report_object);
    spt.api.load_panel(element_eval_panel, 'qc_reports.ElementEvalWdg', {'search_key': inserted_sobject['search_key']});

    spt.app_busy.hide();
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}
            '''
        }

        return behavior

    def get_text_input_wdg(self, field_name, width=200):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(field_name)
        textbox_wdg.set_name(field_name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if hasattr(self, field_name):
            textbox_wdg.set_value(getattr(self, field_name))

        return textbox_wdg

    def get_name_section(self):
        section_div = DivWdg()

        name_wdg = self.get_text_input_wdg('name')

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
        client_sel.set_id('client')
        client_sel.add_style('width', '135px')
        client_sel.add_empty_option()

        client_search = Search('twog/client')
        clients = client_search.get_sobjects()

        for client in clients:
            client_sel.append_option(client.get_value('name'), client.get_code())

        if hasattr(self, 'client'):
            client_sel.set_value(self.client)

        return client_sel

    def get_status_select(self):
        status_sel = SelectWdg('status_select')
        status_sel.set_id('status')
        status_sel.add_style('width', '135px')
        status_sel.add_empty_option()

        statuses = ('Approved', 'Rejected')

        for status in statuses:
            status_sel.append_option(status, status)

        if hasattr(self, 'status'):
            status_sel.set_value(self.status)

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

        try:
            date = self.date
            date_calendar_wdg.set_value(date)
        except AttributeError:
            pass

        return date_calendar_wdg

    def get_style_select(self):
        style_sel = SelectWdg('style_select')
        style_sel.set_id('style')
        style_sel.add_style('width: 135px;')
        style_sel.add_empty_option()

        for style in ('Technical', 'Spot QC', 'Mastering'):
            style_sel.append_option(style, style)

        try:
            style_sel.set_value(self.style_sel)
        except AttributeError:
            pass

        return style_sel

    def get_bay_select(self):
        bay_sel = SelectWdg('bay_select')
        bay_sel.set_id('bay')
        bay_sel.add_style('width', '135px')
        bay_sel.add_empty_option()

        for i in range(1, 13):
            bay_sel.append_option('Bay %s' % i, 'Bay %s' % i)

        try:
            bay_sel.set_value(self.bay)
        except AttributeError:
            pass

        return bay_sel

    def get_machine_select(self):
        machine_sel = SelectWdg('machine_select')
        machine_sel.set_id('machine')
        machine_sel.add_style('width', '135px')
        machine_sel.add_empty_option()

        machine_search = Search('twog/machine')
        machines = machine_search.get_sobjects()

        for machine in machines:
            machine_sel.append_option(machine.get_value('name'), machine.get_code())

        try:
            machine_sel.set_value(self.machine)
        except AttributeError:
            pass

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

        section_span.add(self.get_text_input_wdg('title_data', 400))

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

        try:
            format_sel.set_value(self.format_data)
        except AttributeError:
            pass

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

        try:
            standard_select.set_value(self.standard)
        except AttributeError:
            pass

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
        frame_rate_select.set_id('frame_rate')
        frame_rate_select.add_style('width', '153px')
        frame_rate_select.add_style('display', 'inline-block')
        frame_rate_select.add_empty_option()

        frame_rate_search = Search('twog/frame_rate')
        frame_rates = frame_rate_search.get_sobjects()
        frame_rates = [frame_rate.get_value('name') for frame_rate in frame_rates]

        for frame_rate in frame_rates:
            frame_rate_select.append_option(frame_rate, frame_rate)

        try:
            frame_rate_select.set_value(self.frame_rate)
        except AttributeError:
            pass

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

    def get_file_name_section(self):
        section_div = DivWdg()

        section_div.add(self.get_file_name_input_wdg())

        return section_div

    def get_file_name_input_wdg(self):
        section_span = SpanWdg()

        section_span.add('File Name: ')
        section_span.add(self.get_text_input_wdg('file_name', 600))

        return section_span

    def get_program_format_table(self):
        program_format_table = Table()
        program_format_table.add_style('float', 'left')

        program_format_table.add_row()
        program_format_table.add_header('Program Format')
        program_format_table.add_header()

        text_input_name_id_pairs = [
            ('Roll-up (blank)', 'roll_up_blank'),
            ('Bars/Tone', 'bars_tone'),
            ('Black/Silence', 'black_silence_1'),
            ('Slate/Silence', 'slate_silence'),
            ('Black/Silence', 'black_silence_2'),
            ('Start of Program', 'start_of_program'),
            ('End of Program', 'end_of_program')
        ]

        self.setup_table_rows_with_input_boxes(program_format_table, text_input_name_id_pairs)

        return program_format_table

    def setup_table_rows_with_input_boxes(self, table, text_input_name_id_pairs):

        for text_input_name_id_pair in text_input_name_id_pairs:
            table.add_row()

            text_input_name = str(text_input_name_id_pair[0])
            text_input_id = str(text_input_name_id_pair[1])

            table.add_cell(text_input_name)
            table.add_cell(self.get_text_input_wdg(text_input_id, 300))

    def get_video_measurements_table(self):
        video_measurements_table = Table()

        video_measurements_table.add_row()
        video_measurements_table.add_header('Video Measurements')

        text_input_name_id_pairs = [
            ('Active Video Begins', 'active_video_begins'),
            ('Active Video Ends', 'active_video_ends'),
            ('Horizontal Blanking', 'horizontal_blanking'),
            ('Luminance Peak', 'luminance_peak'),
            ('Chroma Peak', 'chroma_peak'),
            ('Head Logo', 'head_logo'),
            ('Tail Logo', 'tail_logo')
        ]

        self.setup_table_rows_with_input_boxes(video_measurements_table, text_input_name_id_pairs)

        return video_measurements_table

    def get_element_profile_table(self):
        element_profile_table = Table()

        element_profile_table.add_row()
        element_profile_table.add_header('Element Profile')

        element_profile_table.add_row()
        element_profile_table.add_cell('Total Runtime')
        element_profile_table.add_cell(self.get_text_input_wdg('total_runtime', 300))
        element_profile_table.add_cell('Language')
        element_profile_table.add_cell(self.get_text_input_wdg('language', 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('TV/Feature/Trailer')
        element_profile_table.add_cell(self.get_text_input_wdg('tv_feature_trailer', 300))
        element_profile_table.add_cell('(CC)/Subtitles')
        element_profile_table.add_cell(self.get_text_input_wdg('cc_subtitles', 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Video Aspect Ratio')
        element_profile_table.add_cell(self.get_video_aspect_ratio_select_wdg())
        element_profile_table.add_cell('VITC')
        element_profile_table.add_cell(self.get_text_input_wdg('vitc', 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Textless @ Tail')
        element_profile_table.add_cell(self.get_text_input_wdg('textless_tail', 300))
        element_profile_table.add_cell('Source Barcode')
        element_profile_table.add_cell(self.get_text_input_wdg('source_barcode', 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Notices')
        element_profile_table.add_cell(self.get_text_input_wdg('notices', 300))
        element_profile_table.add_cell('Element QC Barcode')
        element_profile_table.add_cell(self.get_text_input_wdg('element_qc_barcode', 300))

        element_profile_table.add_row()
        element_profile_table.add_cell('Label')
        element_profile_table.add_cell(self.get_label_select_wdg())
        element_profile_table.add_cell('Record Date')
        element_profile_table.add_cell(self.get_record_date_calendar_wdg())

        return element_profile_table

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

        if hasattr(self, 'video_aspect_ratio'):
            video_aspect_ratio_sel.set_value(self.video_aspect_ratio)

        return video_aspect_ratio_sel

    def get_label_select_wdg(self):
        label_select_wdg = SelectWdg('label')
        label_select_wdg.set_id('label')
        label_select_wdg.add_style('width', '300px')
        label_select_wdg.add_style('display', 'inline-block')
        label_select_wdg.add_empty_option()

        for label in ('Good', 'Fair', 'Poor'):
            label_select_wdg.append_option(label, label)

        if hasattr(self, 'label'):
            label_select_wdg.set_value(self.label)

        return label_select_wdg

    def get_record_date_calendar_wdg(self):
        record_date_calendar_wdg = CalendarInputWdg("record_date")
        record_date_calendar_wdg.set_option('show_activator', 'true')
        record_date_calendar_wdg.set_option('show_time', 'false')
        record_date_calendar_wdg.set_option('width', '300px')
        record_date_calendar_wdg.set_option('id', 'record_date')
        record_date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

        if hasattr(self, 'record_date'):
            record_date_calendar_wdg.set_value(self.record_date)

        return record_date_calendar_wdg

    def get_general_comments_section(self):
        general_comments_div = DivWdg()
        general_comments_div.add_style('margin', '10px')
        general_comments_wdg = TextAreaWdg()
        general_comments_wdg.set_id('general_comments')
        general_comments_wdg.set_input_prefix('test')

        if hasattr(self, 'general_comments'):
            general_comments_wdg.set_value(self.general_comments)

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
        save_button.add_behavior(self.get_save_behavior(self.element_eval_sobject.get_code()))

        section_span.add(save_button)

        return section_span

    def get_save_as_new_button(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        save_as_new_button = ButtonNewWdg(title='Save As', icon='NEW')
        save_as_new_button.add_class('save_as_new_button')
        save_as_new_button.add_behavior(self.get_save_as_new_behavior())

        section_span.add(save_as_new_button)

        return section_span

    def get_display(self):
        # This will be the main <div> that everything else goes into
        main_wdg = DivWdg()
        main_wdg.set_id('element_eval_panel')

        main_wdg.add(self.get_name_section())

        main_wdg.add(self.get_client_section())

        main_wdg.add(self.get_operator_section())
        main_wdg.add(self.get_title_section())
        main_wdg.add(self.get_season_section())
        main_wdg.add(self.get_episode_section())
        main_wdg.add(self.get_version_section())
        main_wdg.add(self.get_file_name_section())

        main_wdg.add(self.get_program_format_table())
        main_wdg.add(self.get_video_measurements_table())
        main_wdg.add(self.get_element_profile_table())

        if hasattr(self, 'element_eval_sobject') and self.element_eval_sobject:
            main_wdg.add(AudioLinesTableWdg(element_evaluation_code=self.element_eval_sobject.get_code()))

        main_wdg.add(self.get_general_comments_section())

        if hasattr(self, 'element_eval_sobject') and self.element_eval_sobject:
            main_wdg.add(ElementEvalLinesWdg(element_evaluation_code=self.element_eval_sobject.get_code()))
            main_wdg.add(self.get_save_button())

        main_wdg.add(self.get_save_as_new_button())

        return main_wdg
