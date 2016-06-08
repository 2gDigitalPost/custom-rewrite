from tactic.ui.common import BaseTableElementWdg

from pyasm.prod.biz import ProdSetting
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, TextWdg, CheckboxWdg


def get_bay_select():
    bay_sel = SelectWdg('bay_select')
    bay_sel.add_attr('id', 'bay')
    bay_sel.add_style('width', '135px')
    bay_sel.add_empty_option()

    for i in range(1, 13):
        bay_sel.append_option('Bay %s' % i, 'Bay %s' % i)
    # if my.element.get('bay') not in [None, '']:
    #     bay_sel.set_value(my.element.get('bay'))

    return bay_sel


def get_machine_select():
    machine_sel = SelectWdg('machine_select')
    machine_sel.add_attr('id', 'machine_number')
    machine_sel.add_style('width: 135px;')
    machine_sel.add_empty_option()

    for m in ('VTR221', 'VTR222', 'VTR223', 'VTR224', 'VTR225', 'VTR231', 'VTR232', 'VTR233', 'VTR234',
                       'VTR235', 'VTR251', 'VTR252', 'VTR253', 'VTR254', 'VTR255', 'VTR261', 'VTR262', 'VTR263',
                       'VTR264', 'VTR265', 'VTR281', 'VTR282', 'VTR283', 'VTR284', 'VTR285', 'FCP01', 'FCP02', 'FCP03',
                       'FCP04', 'FCP05', 'FCP06', 'FCP07', 'FCP08', 'FCP09', 'FCP10', 'FCP11', 'FCP12', 'Amberfin',
                       'Clipster', 'Stradis'):
        machine_sel.append_option(m, m)
    # if my.element.get('machine_number') not in [None, '']:
    #     machine_sel.set_value(my.element.get('machine_number'))

    return machine_sel


def get_style_select():
    style_sel = SelectWdg('style_select')
    style_sel.add_attr('id', 'style')
    style_sel.add_style('width: 135px;')
    style_sel.add_empty_option()

    for s in ('Technical', 'Spot QC', 'Mastering'):
        style_sel.append_option(s, s)
    # if my.element.get('style') not in [None, '']:
    #     style_sel.set_value(my.element.get('style'))

    return style_sel


def get_text_input_wdg(name, width=200):
    textbox_wdg = TextWdg(name)
    textbox_wdg.set_id(name)
    textbox_wdg.add_style('width', '{0}px'.format(width))

    return textbox_wdg


def get_title_input_wdg():
    section_div = DivWdg()

    section_div.add('Title: ')
    section_div.add(get_text_input_wdg('title', 400))

    return section_div


def get_format_section():
    section_div = DivWdg()

    section_div.add('Format: ')
    section_div.add(get_format_select_wdg())

    return section_div


def get_format_select_wdg():
    format_sel = SelectWdg('format_select')
    format_sel.add_attr('id', 'format')
    format_sel.add_style('width: 153px;')
    format_sel.append_option('--Select--', '')
    for f in ('Electronic/File', 'File - ProRes', 'File - MXF', 'File - MPEG', 'File - WAV', 'DBC', 'D5', 'HDCAM SR',
              'NTSC', 'PAL'):
        format_sel.append_option(f, f)
    # if my.element.get('format') not in [None, '']:
        # format_sel.set_value(my.element.get('format'))

    return format_sel



class ElementEvalWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.formats = ['Electronic/File', 'File - ProRes', 'File - MXF', 'File - MPEG', 'File - WAV','DBC', 'D5',
                      'HDCAM SR', 'NTSC', 'PAL']
        my.frame_rates = ProdSetting.get_seq_by_key('frame_rates')
        my.machines = ['VTR221', 'VTR222', 'VTR223', 'VTR224', 'VTR225', 'VTR231', 'VTR232', 'VTR233', 'VTR234',
                       'VTR235', 'VTR251', 'VTR252', 'VTR253', 'VTR254', 'VTR255', 'VTR261', 'VTR262', 'VTR263',
                       'VTR264', 'VTR265', 'VTR281', 'VTR282', 'VTR283', 'VTR284', 'VTR285', 'FCP01', 'FCP02', 'FCP03',
                       'FCP04', 'FCP05', 'FCP06', 'FCP07', 'FCP08', 'FCP09', 'FCP10', 'FCP11', 'FCP12', 'Amberfin',
                       'Clipster', 'Stradis']
        my.styles = ['Technical', 'Spot QC', 'Mastering']
        my.aspect_ratios = ['16x9 1.33',
                            '16x9 1.33 Pan & Scan',
                            '16x9 1.78 Anamorphic',
                            '16x9 1.78 Full Frame',
                            '16x9 1.85 Letterbox',
                            '16x9 1.85 Matted',
                            '16x9 1.85 Matted Anamorphic',
                            '16x9 2.00 Letterbox',
                            '16x9 2.10 Letterbox',
                            '16x9 2.20 Letterbox',
                            '16x9 2.35 Anamorphic',
                            '16x9 2.35 Letterbox',
                            '16x9 2.40 Letterbox',
                            '16x9 2.55 Letterbox',
                            '4x3 1.33 Full Frame',
                            '4x3 1.78 Letterbox',
                            '4x3 1.85 Letterbox',
                            '4x3 2.35 Letterbox',
                            '4x3 2.40 Letterbox']
        my.standards = ['625', '525', '720', '1080 (4:4:4)', '1080', 'PAL', 'NTSC', '-']
        my.element = None
        my.element_lines = None

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

    def txtbox(my, name, width=200, js=False):
        txt = TextWdg(name)
        txt.add_attr('id', name)
        txt.add_style('width: {0}px;'.format(width))
        txt.set_value(my.element.get(name))

        if js:
            txt.add_behavior(my.get_add_dots())

        return txt

    def set_other_reports_table(self, other_reports, table_title):
        other_reports_table = Table()

        if other_reports:
            other_reports_table.add_style('width', '100%')
            other_reports_table.add_style('border', '1px solid gray')
            other_reports_table.add_style('margin', '3px')

            other_reports_table.add_row()

            title_cell = other_reports_table.add_cell(table_title)
            title_cell.add_style('font-weight', 'bold')
            title_cell.add_style('text-decoration', 'underline')
            title_cell.add_style('text-align', 'center')
            title_cell.add_style('padding', '4px')

            columns = ('Code', 'Language', 'Operator', 'Conclusion', 'Format', 'Standard', 'Frame Rate', 'Timestamp')
            header_row = other_reports_table.add_row()

            for column in columns:
                header_cell = other_reports_table.add_header(data=column, row=header_row)
                header_cell.add_style('border', '1px solid gray')
                header_cell.add_style('padding', '4px')

            for report in other_reports:
                code = report.get('code')
                work_order_code = report.get('work_order_code')
                language = report.get('language')
                operator = report.get('operator')
                conclusion = report.get('conclusion')
                file_format = report.get('format')
                standard = report.get('standard')
                frame_rate = report.get('frame_rate')
                timestamp = report.get('timestamp')

                click_row = other_reports_table.add_row()
                click_row.add_attr('element_code', code)
                click_row.add_attr('work_order_code', work_order_code)
                click_row.add_style('cursor', 'pointer')
                click_row.add_behavior(self.get_click_row(work_order_code, code))

                for cell_data in [code, language, operator, conclusion, file_format, standard, frame_rate, timestamp]:
                    table_body_cell = other_reports_table.add_cell(data=cell_data, row=click_row)
                    table_body_cell.add_style('border', '1px solid gray')
                    table_body_cell.add_style('padding', '4px')

        return other_reports_table

    @staticmethod
    def set_image_and_address(main_wdg):
        image_cell = '<img src="/opt/spt/custom/qc_reports/2GLogo_small4.png"/>'
        image_div = DivWdg()
        image_div.add(image_cell)
        image_div.add_style('float', 'left')
        image_div.add_style('margin', '5px')

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

        main_wdg.add(image_div)
        main_wdg.add(address_div)

    @staticmethod
    def get_client_name(main_wdg, client_name):
        client_name_div = DivWdg(client_name)
        client_name_div.add_style('font-size', '40px')
        client_name_div.add_style('display', 'inline-block')
        client_name_div.add_style('padding', '10px')

        return client_name_div

    @staticmethod
    def get_approved_rejected_checkboxes(main_wdg, conclusion):
        acr_s = ['APPROVED', 'REJECTED']
        acr = Table()
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

    @staticmethod
    def get_operator_section():
        majtbl = Table()
        majtbl.add_attr('class', 'majtbl')
        majtbl.add_row()
        majtbl.add_header('DATE')
        majtbl.add_header('OPERATOR')
        majtbl.add_header('STYLE')
        majtbl.add_header('BAY')
        majtbl.add_header('MACHINE #')
        majtbl.add_row()

        majtbl.add_cell(get_text_input_wdg('timestamp'))
        majtbl.add_cell(get_text_input_wdg('operator'))
        majtbl.add_cell(get_style_select())
        majtbl.add_cell(get_bay_select())
        majtbl.add_cell(get_machine_select())

        return majtbl

    @staticmethod
    def get_title_section():
        section_div = DivWdg()

        section_div.add(get_title_input_wdg())
        section_div.add(get_format_section())

        return section_div

    def get_display(self):
        # This will be the main <div> that everything else goes into
        main_wdg = DivWdg()

        self.set_image_and_address(main_wdg)
        main_wdg.add(self.get_client_name(main_wdg, 'Netflix'))
        main_wdg.add(self.get_approved_rejected_checkboxes(main_wdg, 'APPROVED'))
        main_wdg.add(self.get_operator_section())
        main_wdg.add(self.get_title_section())

        return main_wdg
