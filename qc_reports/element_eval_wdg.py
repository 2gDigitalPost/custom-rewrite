from tactic.ui.common import BaseTableElementWdg
from tactic.ui.input import TextInputWdg, TextAreaInputWdg
from tactic.ui.widget import CalendarInputWdg, ButtonNewWdg

from pyasm.search import Search
from pyasm.web import Table, DivWdg, SpanWdg
from pyasm.widget import SelectWdg, CheckboxWdg


def get_text_input_wdg(name, width=200, text=None):
    textbox_wdg = TextInputWdg()
    textbox_wdg.set_id(name)
    textbox_wdg.set_name(name)
    textbox_wdg.add_style('width', '{0}px'.format(width))

    if text:
        textbox_wdg.set_value(text)

    return textbox_wdg


def get_video_aspect_ratio_select_wdg():
    video_aspect_ratio_sel = SelectWdg('video_aspect_ratio_select')
    video_aspect_ratio_sel.set_id('video_aspect_ratio')
    video_aspect_ratio_sel.add_style('width', '300px')
    video_aspect_ratio_sel.add_style('display', 'inline-block')
    video_aspect_ratio_sel.add_empty_option()

    for video_aspect_ratio in ('16x9 1.33', '16x9 1.33 Pan & Scan', '16x9 1.78 Anamorphic', '16x9 1.78 Full Frame',
                               '16x9 1.85 Letterbox', '16x9 1.85 Matted', '16x9 1.85 Matted Anamorphic',
                               '16x9 2.00 Letterbox', '16x9 2.10 Letterbox', '16x9 2.20 Letterbox',
                               '16x9 2.35 Anamorphic', '16x9 2.35 Letterbox', '16x9 2.40 Letterbox',
                               '16x9 2.55 Letterbox', '4x3 1.33 Full Frame', '4x3 1.78 Letterbox', '4x3 1.85 Letterbox',
                               '4x3 2.35 Letterbox', '4x3 2.40 Letterbox'):
        video_aspect_ratio_sel.append_option(video_aspect_ratio, video_aspect_ratio)

    return video_aspect_ratio_sel


def get_label_select_wdg():
    label_select_wdg = SelectWdg('label')
    label_select_wdg.set_id('label')
    label_select_wdg.add_style('width', '300px')
    label_select_wdg.add_style('display', 'inline-block')
    label_select_wdg.add_empty_option()

    for label in ('Good', 'Fair', 'Poor'):
        label_select_wdg.append_option(label, label)

    return label_select_wdg


def get_record_date_calendar_wdg():
    record_date_calendar_wdg = CalendarInputWdg("record_date")
    record_date_calendar_wdg.set_option('show_activator', 'true')
    record_date_calendar_wdg.set_option('show_time', 'false')
    record_date_calendar_wdg.set_option('width', '300px')
    record_date_calendar_wdg.set_option('id', 'record_date')
    record_date_calendar_wdg.set_option('display_format', 'MM/DD/YYYY')

    return record_date_calendar_wdg


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


def get_audio_configuration_table():
    audio_configuration_table = Table()

    audio_configuration_table.add_row()
    audio_configuration_table.add_header('Audio Configuration')

    audio_configuration_table.add_row()
    audio_configuration_table.add_header('Channel')
    audio_configuration_table.add_header('Content')
    audio_configuration_table.add_header('Tone')
    audio_configuration_table.add_header('Peak')

    for iterator in range(8):
        audio_configuration_table.add_row()
        audio_configuration_table.add_cell(get_text_input_wdg('channel-{0}'.format(iterator), 150))
        audio_configuration_table.add_cell(get_text_input_wdg('content-{0}'.format(iterator), 150))
        audio_configuration_table.add_cell(get_text_input_wdg('tone-{0}'.format(iterator), 150))
        audio_configuration_table.add_cell(get_text_input_wdg('peak-{0}'.format(iterator), 150))

    return audio_configuration_table


def get_general_comments_section():
    general_comments_div = DivWdg()
    general_comments_wdg = TextAreaInputWdg()

    general_comments_div.add('General Comments')
    general_comments_div.add(general_comments_wdg)

    return general_comments_div


def get_audio_configuration_add_behavior():
    behavior = {
        'css_class': 'clickme',
        'type': 'click_up',
        'cbjs_action': '''

        '''
                }

    return behavior


class ElementEvalWdg(BaseTableElementWdg):

    def init(self):
        print(self.get_kwargs())

        report_data = self.get_kwargs().get('report_data')
        print(report_data)

        if report_data:
            self.date = report_data.get('date')
            self.operator = report_data.get('operator')
            self.style_sel = report_data.get('style') # self.style is already used in the super class
            self.bay = report_data.get('bay')
            self.machine_number = report_data.get('machine_number')
            self.title_data = report_data.get('title_data') # self.title is already used in the super class
            self.format_data = report_data.get('format') # 'format' is a reserved word in Python
            self.season = report_data.get('season')
            self.standard = report_data.get('standard')
            self.episode = report_data.get('episode')
            self.frame_rate = report_data.get('frame_rate')
            self.version = report_data.get('version')
            self.po_number = report_data.get('po_number')
            self.file_name = report_data.get('file_name')
            self.roll_up_blank = report_data.get('roll_up_blank')
            self.bars_tone = report_data.get('bars_tone')
            self.black_silence_1 = report_data.get('black_silence_1')
            self.slate_silence = report_data.get('slate_silence')
            self.black_silence_2 = report_data.get('black_silence_2')
            self.start_of_program = report_data.get('start_of_program')
            self.end_of_program = report_data.get('end_of_program')
            self.active_video_begins = report_data.get('active_video_begins')
            self.active_video_ends = report_data.get('active_video_ends')
            self.horizontal_blanking = report_data.get('horizontal_blanking')
            self.luminance_peak = report_data.get('luminance_peak')
            self.chroma_peak = report_data.get('chroma_peak')
            self.head_logo = report_data.get('head_logo')
            self.tail_logo = report_data.get('tail_logo')
            self.total_runtime = report_data.get('total_runtime')
            self.language = report_data.get('language')
            self.tv_feature_trailer = report_data.get('tv_feature_trailer')
            self.cc_subtitles = report_data.get('cc_subtitles')
            self.video_aspect_ratio = report_data.get('video_aspect_ratio')
            self.vitc = report_data.get('vitc')
            self.textless_tail = report_data.get('textless_tail')
            self.source_barcode = report_data.get('source_barcode')
            self.notices = report_data.get('notices')
            self.element_qc_barcode = report_data.get('element_qc_barcode')
            self.label = report_data.get('label')
            self.record_date = report_data.get('record_date')
        else:
            self.title_code = self.get_kwargs().get('title_code')

            title_sobject_search = Search('twog/title')
            title_sobject_search.add_code_filter(self.title_code)
            self.title_sobject = title_sobject_search.get_sobject()

    @staticmethod
    def get_reload_behavior():
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {

    // First row values
    var date = document.getElementsByName("date")[0].value;
    var operator = document.getElementsByName("operator")[0].value;
    var style = document.getElementById("style").value;
    var bay = document.getElementById("bay").value;
    var machine_number = document.getElementById("machine_number").value;

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

    var qc_report_object = {
        'date': date,
        'operator': operator,
        'style': style,
        'bay': bay,
        'machine_number': machine_number,
        'title_data': title_data,
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
        'record_date': record_date
    };

    var board_table = document.getElementById('element_eval_panel');

    spt.app_busy.show("Refreshing...");
    spt.api.load_panel(board_table, 'qc_reports.ElementEvalWdg', {'report_data': qc_report_object});
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
    def get_save_bvr(wo_code, ell_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        function loop_dict(dictionary){
                            //var keys = [];
                            for (var key in dictionary) {
                              if (dictionary.hasOwnProperty(key)) {
                                //keys.push(key);
                                alert(key + ': ' + dictionary[key]);
                              }
                            }
                        }
                        try{
                          wo_code = '%s';
                          ell_code = '%s';
                          top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                          top_el = null;
                          for(var r = 0; r < top_els.length; r++){
                              if(top_els[r].getAttribute('element_code') == ell_code){
                                  top_el = top_els[r];
                              }
                          }
                          big_els = document.getElementsByClassName('big_ol_element_wdg_' + wo_code);
                          big_el = null;
                          for(var r = 0; r < big_els.length; r++){
                              if(big_els[r].getAttribute('element_code') == ell_code){
                                  big_el = big_els[r];
                              }
                          }
                          element_code_old = top_el.getAttribute('element_code');
                          var server = TacticServerStub.get();
                          whole_status = '';
                          stat_els = top_el.getElementsByClassName('spt_input');
                          for(var r = 0; r < stat_els.length; r++){
                              name = stat_els[r].getAttribute('name');
                              if(name.indexOf('marked_') != -1 && stat_els[r].getAttribute('type') == 'checkbox'){
                                  if(stat_els[r].checked){
                                      if(whole_status == ''){
                                          whole_status = name.replace('marked_','');
                                      }else{
                                          whole_status = whole_status + ',' + name.replace('marked_','');
                                      }
                                  }
                              }
                          }
                          if(whole_status == ''){
                              spt.alert('You must first tell us if it was Approved, Rejected, or if there is a Special Condition. Do This by using the checkboxes in the upper-right');
                          }else{
                              spt.app_busy.show('Saving this report...');
                              work_order = server.eval("@SOBJECT(twog/work_order['code','" + wo_code + "'])")[0];
                              sources = server.eval("@SOBJECT(twog/title_origin['title_code','" + work_order.title_code + "'])");
                              source_codes = '';
                              for(var r = 0; r < sources.length; r++){
                                  if(source_codes == ''){
                                      source_codes = sources[r].source_code;
                                  }else{
                                      source_codes = source_codes + ',' + sources[r].source_code;
                                  }
                              }
                              new_data_fields = ['description','timestamp','operator','bay','machine_number','client_name','title','season','episode','version','style','format','standard','po_number','style','aspect_ratio','frame_rate','roll_up','bars_tone','black_silence_1','slate_silence','black_silence_2','start_of_program','end_of_program','roll_up_f','bars_tone_f','black_silence_1_f','slate_silence_f','black_silence_2_f','start_of_program_f','end_of_program_f','active_video_begins','active_video_ends','horizontal_blanking','video_peak','chroma_peak','total_runtime','tv_feature_trailer','textless_at_tail','cc_subtitles','vitc','record_date','language','label','head_logo','tail_logo','notices','record_vendor','vendor_id','file_name'];
                              new_data = {};
                              for(var r = 0; r < new_data_fields.length; r++){
                                  the_field = new_data_fields[r];
                                  the_element = top_el.getElementById(the_field);
                                  if(the_element != null){
                                    new_data[the_field] = the_element.value;
                                  }
                              }
                              decs = ['dec_a1','dec_a2','dec_a3','dec_a4','dec_b1','dec_b2','dec_b3','dec_b4','dec_c1','dec_c2','dec_c3','dec_c4','dec_d1','dec_d2','dec_d3','dec_d4'];
                              for(var r = 0; r < decs.length; r++){
                                  new_data[decs[r]] = '';
                              }
                              date_els = top_el.getElementsByClassName('spt_calendar_input');
                              record_date_el = null;
                              for(var w = 0; w < date_els.length; w++){
                                  if(date_els[w].name == 'record_date'){
                                      record_date_el = date_els[w];
                                  }
                              }
                              record_date = record_date_el.value;
                              new_data['record_date'] = record_date;
                              new_data['login'] = new_data['operator'];
                              new_data['client_code'] = work_order.client_code;
                              new_data['title_code'] = work_order.title_code;
                              new_data['order_code'] = work_order.order_code;
                              new_data['work_order_code'] = wo_code;
                              new_data['conclusion'] = whole_status;
                              new_data['source_code'] = source_codes;
                              new_data['wo_name'] = work_order.process;
                              new_data['type'] = '';
                              new_data['title_type'] = '';
                              new_data['setup'] = '';
                              new_data['vertical_blanking'] = '';
                              new_data['timecodes'] = '';
                              new_data['comp_mne_sync'] = '';
                              new_data['comp_mne_phase'] = '';
                              new_data['missing_mne'] = '';
                              new_data['average_dialogue'] = '';
                              new_data['ltc'] = '';
                              new_data['control_track'] = '';
                              new_element_eval = null;
                              if(element_code_old == ''){
                                  new_element_eval = server.insert('twog/element_eval', new_data);
                              }else{
                                  new_element_eval = server.update(server.build_search_key('twog/element_eval', element_code_old), new_data);
                              }
                              if(new_element_eval.code != ''){
                                  lines = big_el.getElementsByClassName('element_lines');
                                  for(var r = 0; r < lines.length; r++){
                                      if(lines[r].style.display != 'none'){
                                          rowct = lines[r].getAttribute('line');
                                          old_code = lines[r].getAttribute('code');
                                          timecode_in = big_el.getElementById('timecode_in-' + rowct).value;
                                          field_in = big_el.getElementById('field_in-' + rowct).value;
                                          timecode_out = big_el.getElementById('timecode_out-' + rowct).value;
                                          field_out = big_el.getElementById('field_out-' + rowct).value;
                                          //media_type = big_el.getElementById('media_type-' + rowct).value;
                                          description_ele = big_el.getElementById('description-' + rowct);
                                          description_style = '';
                                          if(description_ele.style.fontWeight == 'bold'){
                                              description_style = 'b';
                                          }
                                          if(description_ele.style.fontStyle == 'italic'){
                                              description_style = description_style + 'i';
                                          }
                                          description = description_ele.value;
                                          type_code = big_el.getElementById('type_code-' + rowct).value;
                                          scale = big_el.getElementById('scale-' + rowct).value;
                                          in_source = big_el.getElementById('in_source-' + rowct).value;
                                          in_safe = big_el.getElementById('in_safe-' + rowct).value;
                                          sector_or_channel = big_el.getElementById('sector_or_channel-' + rowct).value;
                                          ordering = big_el.getElementById('ordering-' + rowct);
                                          element_line = {'description': description, 'login': new_data['operator'], 'element_eval_code': new_element_eval.code, 'order_code': work_order.order_code, 'title_code': work_order.title_code, 'work_order_code': wo_code, 'timecode_in': timecode_in, 'field_in': field_in, 'timecode_out': timecode_out, 'field_out': field_out, 'type_code': type_code, 'scale': scale, 'sector_or_channel': sector_or_channel, 'in_source': in_source, 'in_safe': in_safe, 'source_code': source_codes, 'description_style': description_style}
                                          if(ordering){
                                              oval = ordering.value;
                                              if(oval == null){
                                                  oval = '';
                                              }
                                              element_line['ordering'] = oval;
                                          }
                                          //loop_dict(element_line);
                                          if(description != '' && timecode_in != ''){
                                              if(old_code == ''){
                                                  server.insert('twog/element_eval_lines', element_line);
                                              }else{
                                                  server.update(server.build_search_key('twog/element_eval_lines', old_code), element_line);
                                              }
                                          }
                                      }
                                  }
                                  //This needs to be for the barcode lines
                                  bcs = big_el.getElementsByClassName('element_barcodes');
                                  for(var r = 0; r < bcs.length; r++){
                                      if(bcs[r].style.display != 'none'){
                                          rowct = bcs[r].getAttribute('line');
                                          old_code = bcs[r].getAttribute('code');
                                          barcode = big_el.getElementById('barcode-' + rowct).value;
                                          program_start = big_el.getElementById('program_start-' + rowct).value;
                                          f1 = big_el.getElementById('f1-' + rowct).value;
                                          program_end = big_el.getElementById('program_end-' + rowct).value;
                                          f2 = big_el.getElementById('f2-' + rowct).value;
                                          length = big_el.getElementById('length-' + rowct).value;
                                          label_info = big_el.getElementById('label_info-' + rowct).value;
                                          slate_info = big_el.getElementById('slate_info-' + rowct).value;
                                          element_line = {'barcode': barcode, 'program_start': program_start, 'f1': f1, 'program_end': program_end, 'f2': f2, 'length': length, 'label_info': label_info, 'slate_info': slate_info, 'element_eval_code': new_element_eval.code}
                                          if(barcode != '' && program_start != ''){
                                              if(old_code == ''){
                                                  server.insert('twog/element_eval_barcodes', element_line);
                                              }else{
                                                  server.update(server.build_search_key('twog/element_eval_barcodes', old_code), element_line);
                                              }
                                          }
                                      }
                                  }
                                  //barcode lines end
                                  audio_information_el = big_el.getElementById('audio_information');
                                  num_o_channels = Number(audio_information_el.getAttribute('channels'));
                                  for(var r = 0; r < num_o_channels; r++){
                                      rowct = r;
                                      channel_el = big_el.getElementById('channel-' + rowct);
                                      old_code = channel_el.getAttribute('code');
                                      channel = channel_el.value;
                                      content = big_el.getElementById('content-' + rowct).value;
                                      tone = big_el.getElementById('tone-' + rowct).value;
                                      peak = big_el.getElementById('peak-' + rowct).value;
                                      audio_line = {'channel': channel, 'content': content, 'tone': tone, 'peak': peak, 'element_eval_code': new_element_eval.code};
                                      if(channel != '' && content != ''){
                                          if(old_code == ''){
                                              server.insert('twog/element_eval_audio', audio_line);
                                          }else{
                                              server.update(server.build_search_key('twog/element_eval_audio', old_code), audio_line);
                                          }
                                      }
                                  }
                                  var class_name = 'qc_reports.element_eval_wdg.ElementEvalWdg';
                                  kwargs = {'code': wo_code, 'element_code': new_element_eval.code, 'channels': num_o_channels}
                                  //spt.popup.close(spt.popup.get_popup(bvr.src_el));
                                  //spt.panel.load_popup('Element Evaluation for ' + wo_code, class_name, kwargs);
                                  spt.tab.add_new('ElementEvalWdg_qc_report_for_' + wo_code,'Element Evaluation for ' + wo_code, class_name, kwargs);
                              }
                              spt.app_busy.hide();
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, ell_code)}
        return behavior

    @staticmethod
    def get_clone_report(wo_code, el_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var work_order_code = '%s';
                          var report_code = '%s';
                          var class_name = 'qc_reports.QCReportClonerWdg';
                          kwargs = {'wo_code': work_order_code, 'report_code': report_code, 'type': 'element'}
                          //spt.popup.close(spt.popup.get_popup(bvr.src_el));
                          spt.app_busy.show("Collecting related qc work orders...");
                          spt.panel.load_popup('Clone Report To ... ', class_name, kwargs);
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, el_code)}
        return behavior

    @staticmethod
    def get_print_bvr(wo_code, el_code, type):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        function replaceAll(find, replace, str) {
                          find = find.replace('[','\\\[').replace(']','\\\]').replace('+','\\\+');
                          return str.replace(new RegExp(find, 'g'), replace);
                        }
                        function printExternal(url) {
                            var printWindow = window.open( url, 'Print', 'toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0');
                            printWindow.addEventListener('load', function(){
                                printWindow.print();
                                //printWindow.close();
                            }, true);
                        }
                        try{
                          wo_code = '%s';
                          element_code = '%s';
                          type = '%s';
                          top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                          top_el = null;
                          for(var r = 0; r < top_els.length; r++){
                              if(top_els[r].getAttribute('element_code') == element_code){
                                  top_el = top_els[r];
                              }
                          }
                          title = top_el.getElementById('title').value;
                          episode = top_el.getElementById('episode').value;
                          language = top_el.getElementById('language').value;
                          file_name_str = replaceAll(' ','_',title);
                          if(episode != '' && episode != null){
                              file_name_str = file_name_str + '__' + replaceAll(' ','_',episode);
                          }
                          if(language == '' || language == null){
                              language = 'None_Set';
                          }
                          whole_status = '';
                          stat_els = top_el.getElementsByClassName('spt_input');
                          for(var r = 0; r < stat_els.length; r++){
                              name = stat_els[r].getAttribute('name');
                              if(name.indexOf('marked_') != -1 && stat_els[r].getAttribute('type') == 'checkbox'){
                                  if(stat_els[r].checked){
                                      if(whole_status == ''){
                                          whole_status = name.replace('marked_','');
                                      }else{
                                          whole_status = whole_status + '_' + name.replace('marked_','');
                                      }
                                  }
                              }
                          }
                          file_name_str = file_name_str + '__' + replaceAll(' ','_',language) + '__' + whole_status;
                          file_name_str = replaceAll("\\\'",'',file_name_str);
                          file_name_str = replaceAll("\\\-",'_',file_name_str);
                          file_name_str = replaceAll("\\\.",'',file_name_str);
                          file_name_str = replaceAll("\\\,",'',file_name_str);
                          file_name_str = replaceAll("\\\!",'',file_name_str);
                          file_name_str = replaceAll("\\\?",'',file_name_str);
                          file_name_str = replaceAll("\\\^",'',file_name_str);
                          file_name_str = replaceAll("\\\#",'',file_name_str);
                          file_name_str = replaceAll("\\\&",'_and_',file_name_str);
                          file_name_str = replaceAll("\\\(",'',file_name_str);
                          file_name_str = replaceAll("\\\)",'',file_name_str);
                          file_name_str = replaceAll("\\\*",'',file_name_str);
                          file_name_str = replaceAll("\\\%s",'',file_name_str);
                          file_name_str = replaceAll("\\\$",'',file_name_str);
                          file_name_str = replaceAll("\\\@",'',file_name_str);
                          file_name_str = replaceAll("\\\~",'',file_name_str);
                          file_name_str = replaceAll("\\\`",'',file_name_str);
                          file_name_str = replaceAll("\\\:",'',file_name_str);
                          file_name_str = replaceAll("\\\;",'',file_name_str);
                          file_name_str = replaceAll('\\\"','',file_name_str);
                          file_name_str = replaceAll('\\\<','',file_name_str);
                          file_name_str = replaceAll('\\\>','',file_name_str);
                          file_name_str = replaceAll('\\\/','',file_name_str);
                          file_name_str = replaceAll('\\\|','',file_name_str);
                          file_name_str = replaceAll('\\\}','',file_name_str);
                          file_name_str = replaceAll('\\\{','',file_name_str);
                          file_name_str = replaceAll('\\\=','',file_name_str);
                          var server = TacticServerStub.get();
                          lines = top_el.getElementsByClassName('element_lines');
                          for(var r = 0; r < lines.length; r++){
                              linect = lines[r].getAttribute('line');
                              tc = top_el.getElementById('timecode_in-' + linect);
                              if(tc.value == '' || tc.value == null){
                                  lines[r].style.display = 'none';
                              }
                              ord = top_el.getElementById('ordering-' + linect);
                              if(ord){
                                  ord.style.display = 'none';
                              }
                              killer = top_el.getElementById('killer-' + linect);
                              if(killer){
                                  killer.style.display = 'none';
                              }
                              descriptioner = top_el.getElementById('description-' + linect);
                              if(descriptioner){
                                  descriptioner.setAttribute('width', '520px');
                                  descriptioner.style.width = '520px';
                              }
                          }
                          bcs = top_el.getElementsByClassName('element_barcodes');
                          for(var r = 0; r < bcs.length; r++){
                              linect = bcs[r].getAttribute('line');
                              tc = top_el.getElementById('barcode-' + linect);
                              if(tc.value == '' || tc.value == null){
                                  bcs[r].style.display = 'none';
                              }else{
                                  cells = bcs[r].getElementsByTagName('td');
                                  for(var w = 0; w < cells.length; w++){
                                      if(cells[w].innerHTML == '<b>X</b>'){
                                          cells[w].style.display = 'none';
                                      }
                                  }
                              }
                          }
                          sels = top_el.getElementsByClassName('select_cell');
                          for(var r = 0; r < sels.length; r++){
                              select_el = sels[r].getElementsByTagName('select')[0];
                              offset_width = select_el.offsetWidth;
                              value = select_el.value;
                              sels[r].innerHTML = '<input type="text" value="' + value + '" style="width: ' + offset_width + ';"/>';
                          }
                          tc_shifter = top_el.getElementById('tc_shifter');
                          tc_shifter.style.display = 'none';
                          description_el = top_el.getElementById('description');
                          description_el.setAttribute('cols','110');
                          darkrow = top_el.getElementById('darkrow');
                          darkrow.setAttribute('width','110px');
                          audio_row = top_el.getElementById('audio_row');
                          audio_row.innerHTML = audio_row.innerHTML.replace('- click to change number of channels','');
                          top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                          top_el = null;
                          for(var r = 0; r < top_els.length; r++){
                              if(top_els[r].getAttribute('element_code') == element_code){
                                  top_el = top_els[r];
                              }
                          }
                          new_html = top_el.innerHTML;

                          thing = server.execute_cmd('qc_reports.PrintQCReportWdg', {'html': '<table>' + new_html + '</table>','preppend_file_name': file_name_str, 'type': ''});
                          var url = '/qc_reports/work_orders/' + file_name_str + '.html';
                          printExternal(url);
                          if(element_code != '' && element_code != null){
                              //close, then reload page
                              var class_name = 'qc_reports.element_eval_wdg.ElementEvalWdg';
                              kwargs = {'code': wo_code, 'element_code': element_code}
                              spt.tab.add_new('ElementEvalWdg_qc_report_for_' + wo_code,'Element Evaluation for ' + wo_code, class_name, kwargs);
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, el_code, type, '%')}
        return behavior

    @staticmethod
    def get_new_print_bvr(wo_code, el_code, type):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        function replaceAll(find, replace, str) {
                          find = find.replace('[','\\\[').replace(']','\\\]').replace('+','\\\+');
                          return str.replace(new RegExp(find, 'g'), replace);
                        }
                        function printExternal(url) {
                            var printWindow = window.open( url, 'Print', 'toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0');
                            printWindow.addEventListener('load', function(){
                                printWindow.print();
                                //printWindow.close();
                            }, true);
                        }
                        try{
                          wo_code = '%s';
                          element_code = '%s';
                          type = '%s';
                          top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                          top_el = null;
                          for(var r = 0; r < top_els.length; r++){
                              if(top_els[r].getAttribute('element_code') == element_code){
                                  top_el = top_els[r];
                              }
                          }
                          title = top_el.getElementById('title').value;
                          episode = top_el.getElementById('episode').value;
                          language = top_el.getElementById('language').value;
                          file_name_str = replaceAll(' ','_',title);
                          if(episode != '' && episode != null){
                              file_name_str = file_name_str + '__' + replaceAll(' ','_',episode);
                          }
                          if(language == '' || language == null){
                              language = 'None_Set';
                          }
                          whole_status = '';
                          stat_els = top_el.getElementsByClassName('spt_input');
                          for(var r = 0; r < stat_els.length; r++){
                              name = stat_els[r].getAttribute('name');
                              if(name.indexOf('marked_') != -1 && stat_els[r].getAttribute('type') == 'checkbox'){
                                  if(stat_els[r].checked){
                                      if(whole_status == ''){
                                          whole_status = name.replace('marked_','');
                                      }else{
                                          whole_status = whole_status + '_' + name.replace('marked_','');
                                      }
                                  }
                              }
                          }
                          file_name_str = file_name_str + '__' + replaceAll(' ','_',language) + '__' + whole_status;
                          file_name_str = replaceAll("\\\'",'',file_name_str);
                          file_name_str = replaceAll("\\\-",'_',file_name_str);
                          file_name_str = replaceAll("\\\.",'',file_name_str);
                          file_name_str = replaceAll("\\\,",'',file_name_str);
                          file_name_str = replaceAll("\\\!",'',file_name_str);
                          file_name_str = replaceAll("\\\?",'',file_name_str);
                          file_name_str = replaceAll("\\\^",'',file_name_str);
                          file_name_str = replaceAll("\\\#",'',file_name_str);
                          file_name_str = replaceAll("\\\&",'_and_',file_name_str);
                          file_name_str = replaceAll("\\\(",'',file_name_str);
                          file_name_str = replaceAll("\\\)",'',file_name_str);
                          file_name_str = replaceAll("\\\*",'',file_name_str);
                          file_name_str = replaceAll("\\\%s",'',file_name_str);
                          file_name_str = replaceAll("\\\$",'',file_name_str);
                          file_name_str = replaceAll("\\\@",'',file_name_str);
                          file_name_str = replaceAll("\\\~",'',file_name_str);
                          file_name_str = replaceAll("\\\`",'',file_name_str);
                          file_name_str = replaceAll("\\\:",'',file_name_str);
                          file_name_str = replaceAll("\\\;",'',file_name_str);
                          file_name_str = replaceAll('\\\"','',file_name_str);
                          file_name_str = replaceAll('\\\<','',file_name_str);
                          file_name_str = replaceAll('\\\>','',file_name_str);
                          file_name_str = replaceAll('\\\/','',file_name_str);
                          file_name_str = replaceAll('\\\|','',file_name_str);
                          file_name_str = replaceAll('\\\}','',file_name_str);
                          file_name_str = replaceAll('\\\{','',file_name_str);
                          file_name_str = replaceAll('\\\=','',file_name_str);
                          var server = TacticServerStub.get();
                          lines = top_el.getElementsByClassName('element_lines');
                          for(var r = 0; r < lines.length; r++){
                              linect = lines[r].getAttribute('line');
                              tc = top_el.getElementById('timecode_in-' + linect);
                              if(tc.value == '' || tc.value == null){
                                  lines[r].style.display = 'none';
                              }
                              ord = top_el.getElementById('ordering-' + linect);
                              if(ord){
                                  ord.style.display = 'none';
                              }
                              killer = top_el.getElementById('killer-' + linect);
                              if(killer){
                                  killer.style.display = 'none';
                              }
                              descriptioner = top_el.getElementById('description-' + linect);
                              if(descriptioner){
                                    value = descriptioner.value;

                                    var newDiv = document.createElement('div');
                                    newDiv.innerHTML = value;
                                    newDiv.style.width = '520px';
                                    newDiv.style.borderWidth = '1px';
                                    newDiv.style.borderStyle = 'solid';
                                    newDiv.style.borderColor = 'gray';

                                    descriptioner.parentNode.insertBefore(newDiv, descriptioner);

                                    descriptioner.parentNode.removeChild(descriptioner);
                              }
                          }
                          bcs = top_el.getElementsByClassName('element_barcodes');
                          for(var r = 0; r < bcs.length; r++){
                              linect = bcs[r].getAttribute('line');
                              tc = top_el.getElementById('barcode-' + linect);
                              if(tc.value == '' || tc.value == null){
                                  bcs[r].style.display = 'none';
                              }else{
                                  cells = bcs[r].getElementsByTagName('td');
                                  for(var w = 0; w < cells.length; w++){
                                      if(cells[w].innerHTML == '<b>X</b>'){
                                          cells[w].style.display = 'none';
                                      }
                                  }
                              }
                          }
                          sels = top_el.getElementsByClassName('select_cell');
                          for(var r = 0; r < sels.length; r++){
                              select_el = sels[r].getElementsByTagName('select')[0];
                              offset_width = select_el.offsetWidth;
                              value = select_el.value;
                              sels[r].innerHTML = '<input type="text" value="' + value + '" style="width: ' + offset_width + ';"/>';
                          }
                          tc_shifter = top_el.getElementById('tc_shifter');
                          tc_shifter.style.display = 'none';
                          description_el = top_el.getElementById('description');
                          description_el.setAttribute('cols','110');
                          darkrow = top_el.getElementById('darkrow');
                          darkrow.setAttribute('width','110px');
                          audio_row = top_el.getElementById('audio_row');
                          audio_row.innerHTML = audio_row.innerHTML.replace('- click to change number of channels','');
                          top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                          top_el = null;
                          for(var r = 0; r < top_els.length; r++){
                              if(top_els[r].getAttribute('element_code') == element_code){
                                  top_el = top_els[r];
                              }
                          }
                          new_html = top_el.innerHTML;

                          thing = server.execute_cmd('qc_reports.PrintQCReportWdg', {'html': '<table>' + new_html + '</table>','preppend_file_name': file_name_str, 'type': ''});
                          var url = '/qc_reports/work_orders/' + file_name_str + '.html';
                          printExternal(url);
                          if(element_code != '' && element_code != null){
                              //close, then reload page
                              var class_name = 'qc_reports.element_eval_wdg.ElementEvalWdg';
                              kwargs = {'code': wo_code, 'element_code': element_code}
                              spt.tab.add_new('ElementEvalWdg_qc_report_for_' + wo_code,'Element Evaluation for ' + wo_code, class_name, kwargs);
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, el_code, type, '%')}
        return behavior

    @staticmethod
    def get_click_row(wo_code, el_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var work_order_code = '%s';
                          var element_code = '%s';
                          var class_name = 'qc_reports.element_eval_wdg.ElementEvalWdg';
                          kwargs = {'code': work_order_code, 'element_code': element_code}
                          //spt.popup.close(spt.popup.get_popup(bvr.src_el));
                          //spt.panel.load_popup('Element Evaluation for ' + work_order_code, class_name, kwargs);
                          spt.tab.add_new('ElementEvalWdg_qc_report_for_' + work_order_code,'Element Evaluation for ' + work_order_code, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, el_code)}
        return behavior

    @staticmethod
    def get_add_dots():
        behavior = {'css_class': 'clickme', 'type': 'keyup', 'cbjs_action': '''
                try{
                    var entered = bvr.src_el.value;
                    var new_str = '';
                    entered = entered.replace(/:/g,'');
                    for(var r = 0; r < entered.length; r++){
                        if(r % 2 == 0 && r != 0){
                            new_str = new_str + ':';
                        }
                        new_str = new_str + entered[r];
                    }
                    bvr.src_el.value = new_str;
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    @staticmethod
    def get_delete_report(wo_code, el_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var work_order_code = '%s';
                          var element_code = '%s';
                          if(confirm("Are you sure you want to delete this report?")){
                              if(confirm("Checking again. You really want to delete this report?")){
                                  var server = TacticServerStub.get();
                                  server.retire_sobject(server.build_search_key('twog/element_eval', element_code));
                                  var class_name = 'qc_reports.element_eval_wdg.ElementEvalWdg';
                                  kwargs = {'code': work_order_code}
                                  //spt.popup.close(spt.popup.get_popup(bvr.src_el));
                                  //spt.panel.load_popup('Element Evaluation for ' + work_order_code, class_name, kwargs);
                                  spt.tab.add_new('ElementEvalWdg_qc_report_for_' + work_order_code,'Element Evaluation for ' + work_order_code, class_name, kwargs);
                              }
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, el_code)}
        return behavior

    @staticmethod
    def get_change_channels(wo_code, ell_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          entered = prompt("How many audio channels do you want in this report?");
                          if(isNaN(entered)){
                              alert(entered + " is not a number. Please only enter numbers here.")
                          }else{
                              wo_code = '%s';
                              ell_code = '%s';
                              big_els = document.getElementsByClassName('big_ol_element_wdg_' + wo_code);
                              big_el = null;
                              for(var r = 0; r < big_els.length; r++){
                                  if(big_els[r].getAttribute('element_code') == ell_code){
                                      big_el = big_els[r];
                                  }
                              }
                              audio_table = big_el.getElementById('audio_table');
                              element_eval_code = audio_table.getAttribute('code');
                              send_data = {'code': element_eval_code, 'wo_code': wo_code, 'channels': entered, 'force_it': 'true'};
                              spt.api.load_panel(audio_table, 'qc_reports.ElementEvalAudioWdg', send_data);
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, ell_code)}
        return behavior

    @staticmethod
    def launch_tc_shifter(wo_code, ell_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          wo_code = '%s';
                          ell_code = '%s';
                          var class_name = 'qc_reports.ReportTimecodeShifterWdg';
                          kwargs = {
                                           'wo_code': wo_code,
                                           'ell_code': ell_code
                                   };
                          spt.panel.load_popup('Timecode Shifter', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, ell_code)}
        return behavior

    def get_text_input_wdg(self, name, width=200):
        textbox_wdg = TextInputWdg()
        textbox_wdg.set_id(name)
        textbox_wdg.set_name(name)
        textbox_wdg.add_style('width', '{0}px'.format(width))

        if hasattr(self, name):
            textbox_wdg.set_value(getattr(self, name))
        else:
            if self.title_sobject:
                textbox_wdg.set_value(self.title_sobject.get(name))

        return textbox_wdg

    def get_operator_section(self):
        operator_table = Table()
        operator_table.add_attr('class', 'operator_table')
        operator_table.add_row()
        operator_table.add_header('DATE')
        operator_table.add_header('OPERATOR')
        operator_table.add_header('STYLE')
        operator_table.add_header('BAY')
        operator_table.add_header('MACHINE #')
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
        machine_sel.set_id('machine_number')
        machine_sel.add_style('width', '135px')
        machine_sel.add_empty_option()

        for machine in ('VTR221', 'VTR222', 'VTR223', 'VTR224', 'VTR225', 'VTR231', 'VTR232', 'VTR233', 'VTR234',
                        'VTR235', 'VTR251', 'VTR252', 'VTR253', 'VTR254', 'VTR255', 'VTR261', 'VTR262', 'VTR263',
                        'VTR264', 'VTR265', 'VTR281', 'VTR282', 'VTR283', 'VTR284', 'VTR285', 'FCP01', 'FCP02', 'FCP03',
                        'FCP04', 'FCP05', 'FCP06', 'FCP07', 'FCP08', 'FCP09', 'FCP10', 'FCP11', 'FCP12', 'Amberfin',
                        'Clipster', 'Stradis'):
            machine_sel.append_option(machine, machine)

        try:
            machine_sel.set_value(self.machine_number)
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

        for standard in ('625', '525', '720', '1080 (4:4:4)', '1080', 'PAL', 'NTSC', '-'):
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

        try:
            prefilled_text = self.episode
        except AttributeError:
            if self.title_sobject:
                prefilled_text = self.title_sobject.get('episode')
            else:
                prefilled_text = None

        section_span.add(get_text_input_wdg('episode', 400, prefilled_text))

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

        try:
            prefilled_text = self.version
        except AttributeError:
            if self.title_sobject:
                prefilled_text = self.title_sobject.get('version')
            else:
                prefilled_text = None

        section_span.add(get_text_input_wdg('version', 400, prefilled_text))

        return section_span

    def get_po_number_section(self):
        section_span = SpanWdg()
        section_span.add_style('display', 'inline-block')

        section_span.add('PO #: ')

        try:
            prefilled_text = self.po_number
        except AttributeError:
            if self.title_sobject:
                prefilled_text = self.title_sobject.get('po_number')
            else:
                prefilled_text = None

        section_span.add(get_text_input_wdg('po_number', 100, prefilled_text))

        return section_span

    def get_file_name_section(self):
        section_div = DivWdg()

        section_div.add(self.get_file_name_input_wdg())

        return section_div

    def get_file_name_input_wdg(self):
        section_span = SpanWdg()

        section_span.add('File Name: ')

        try:
            prefilled_text = self.file_name
        except AttributeError:
            if self.title_sobject:
                prefilled_text = self.title_sobject.get('file_name')
            else:
                prefilled_text = None

        section_span.add(get_text_input_wdg('file_name', 600, prefilled_text))

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

    def setup_table_rows_with_input_boxes(self, program_format_table, text_input_name_id_pairs):

        for text_input_name_id_pair in text_input_name_id_pairs:
            program_format_table.add_row()

            text_input_name = str(text_input_name_id_pair[0])
            text_input_id = str(text_input_name_id_pair[1])

            program_format_table.add_cell(text_input_name)

            # Check if the input value is specified in this object
            prefilled_text = getattr(self, text_input_id, None)

            # If no value, check the title_sobject (if it's not there either, prefilled_text will still be None
            if not prefilled_text and self.title_sobject:
                prefilled_text = self.title_sobject.get(text_input_name_id_pair)

            program_format_table.add_cell(get_text_input_wdg(text_input_id, 300, prefilled_text))

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
        element_profile_table.add_cell(get_video_aspect_ratio_select_wdg())
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
        element_profile_table.add_cell(get_label_select_wdg())
        element_profile_table.add_cell('Record Date')
        element_profile_table.add_cell(get_record_date_calendar_wdg())

        return element_profile_table

    def get_display(self):
        # This will be the main <div> that everything else goes into
        main_wdg = DivWdg()
        main_wdg.set_id('element_eval_panel')

        # self.set_image_and_address(main_wdg)
        main_wdg.add(get_image_div())
        main_wdg.add(get_address_div())
        main_wdg.add(get_client_name('Netflix'))
        main_wdg.add(get_approved_rejected_checkboxes('APPROVED'))

        main_wdg.add(self.get_operator_section())
        main_wdg.add(self.get_title_section())
        main_wdg.add(self.get_season_section())
        main_wdg.add(self.get_episode_section())
        main_wdg.add(self.get_version_section())
        main_wdg.add(self.get_file_name_section())

        main_wdg.add(self.get_program_format_table())
        main_wdg.add(self.get_video_measurements_table())
        main_wdg.add(self.get_element_profile_table())
        main_wdg.add(get_audio_configuration_table())

        add_row_button = ButtonNewWdg(title='Add Row', icon='ADD')
        add_row_button.add_class('add_row_button')
        add_row_button.add_behavior(self.get_reload_behavior())

        main_wdg.add(add_row_button)

        main_wdg.add(get_general_comments_section())

        return main_wdg
