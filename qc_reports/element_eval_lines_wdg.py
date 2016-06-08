from tactic_client_lib import TacticServerStub
from tactic.ui.common import BaseTableElementWdg

from pyasm.common import Environment
from pyasm.prod.biz import ProdSetting
from pyasm.web import Table
from pyasm.widget import SelectWdg, TextWdg


class ElementEvalLinesWdg(BaseTableElementWdg):
    def init(my):
        nothing = 'true'

    def get_kill_bvr(my, rowct, wo_code, ell_code, element_eval_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                            var rowct = Number('%s');
                            var wo_code = '%s';
                            var ell_code = '%s';
                            var element_eval_code = '%s';
                            if(confirm("Do you really want to delete this evaluation line?")){
                                server = TacticServerStub.get();
                                server.retire_sobject(server.build_search_key('twog/element_eval_lines',ell_code));
                                top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                                top_el = null;
                                for(var r = 0; r < top_els.length; r++){
                                    if(top_els[r].getAttribute('element_code') == element_eval_code){
                                        top_el = top_els[r];
                                    }
                                }
                                linestbl = top_el.getElementsByClassName('linestbl')[0];
                                element_lines = linestbl.getElementsByClassName('element_lines');
                                for(var r = 0; r < element_lines.length; r++){
                                    if(element_lines[r].getAttribute('line') == rowct){
                                        element_lines[r].innerHTML = '';
                                        element_lines[r].style.display = 'none';
                                    }
                                }
                                send_data = {'rowct': rowct, 'wo_code': wo_code, 'code': ell_code};
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (rowct, wo_code, ell_code, element_eval_code)}
        return behavior

    def get_add_line(my, rowct, wo_code, ell_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                            bvr.src_el.innerHTML = '';
                            var rowct = Number('%s');
                            var wo_code = '%s';
                            var ell_code = '%s';
                            top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                            top_el = null;
                            for(var r = 0; r < top_els.length; r++){
                                if(top_els[r].getAttribute('element_code') == ell_code){
                                    top_el = top_els[r];
                                }
                            }
                            linestbl = top_el.getElementsByClassName('linestbl');
                            lastlinestbl = linestbl[linestbl.length - 1];
                            addportions = top_el.getElementsByClassName('new_element_line');
                            addportion = addportions[addportions.length - 1];
                            addportion.setAttribute('class','element_lines');
                            addportion.setAttribute('line',Number(rowct) + 1);
                            addportion.setAttribute('code','');
                            send_data = {'rowct': rowct + 1, 'wo_code': wo_code, 'code': ell_code, 'reload': 'true'};
                            //send_data = {'rowct': rowct + 1, 'wo_code': wo_code};
                            spt.api.load_panel(addportion, 'qc_reports.ElementEvalLinesWdg', send_data);
                            newrow = lastlinestbl.insertRow(-1);
                            newrow.setAttribute('class','new_element_line');
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (rowct, wo_code, ell_code)}
        return behavior

    def get_select_fillin(my, wo_code, rowct, ell_code):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''
                try{
                   wo_code = '%s';
                   ell_code = '%s';
                   rowct = '%s';
                   top_els = document.getElementsByClassName('printable_element_form_' + wo_code);
                   top_el = null;
                   for(var r = 0; r < top_els.length; r++){
                       if(top_els[r].getAttribute('element_code') == ell_code){
                           top_el = top_els[r];
                       }
                   }
                   this_sel = top_el.getElementById('description-' + rowct);
                   val = this_sel.value;
                   if(val.indexOf('( )') != -1){
                       deets = prompt("Please enter more detail for: " + val);
                       newval = val.replace('( )','(' + deets + ')');
                       inner = this_sel.innerHTML;
                       newinner = inner + '<option value="' + newval + '" selected="selected">' + newval + '</option>';
                       this_sel.innerHTML = newinner;
                   }else if(val.indexOf('...') != -1){
                       deets = prompt("Please enter the new description.");
                       newval = deets;
                       if(val.indexOf('V -') != -1){
                           newval = 'V - ' + newval;
                       }else{
                           newval = 'A - ' + newval;
                       }
                       inner = this_sel.innerHTML;
                       newinner = inner + '<option value="' + newval + '" selected="selected">' + newval + '</option>';
                       this_sel.innerHTML = newinner;
                       server = TacticServerStub.get();
                       server.insert('twog/qc_report_vars', {'type': 'element', 'description': newval});
                   }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, ell_code, rowct)}
        return behavior

    def get_add_dots(my):
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

    def get_alter_text_bold(my):
        behavior = {'type': 'click_up', 'mouse_btn': 'LMB', 'modkeys': 'SHIFT', 'cbjs_action': '''
                try{
                    if(bvr.src_el.style.fontWeight != 'bold'){
                        bvr.src_el.style.fontWeight = 'bold';
                    }else{
                        bvr.src_el.style.fontWeight = 'normal';
                    }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_alter_text_italic(my):
        behavior = {'type': 'click_up', 'mouse_btn': 'LMB', 'modkeys': 'CTRL', 'cbjs_action': '''
                try{
                    if(bvr.src_el.style.fontStyle != 'italic'){
                        bvr.src_el.style.fontStyle = 'italic';
                    }else{
                        bvr.src_el.style.fontStyle = 'normal';
                    }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def txtbox(my, name, val, width='200px', js='no', style=''):
        txt = TextWdg(name)
        txt.add_attr('id',name)
        txt.add_style('width: %s;' % width)
        txt.set_value(val)
        if not style:
            style = ''
        if 'i' in style:
            txt.add_style('font-style: italic;')
        if 'b' in style:
            txt.add_style('font-weight: bold;')
        if js in ['Yes','yes']:
            txt.add_behavior(my.get_add_dots())
        if 'description' in name:
            txt.add_behavior(my.get_alter_text_bold())
            txt.add_behavior(my.get_alter_text_italic())
        return txt

    def get_display(my):
        login = Environment.get_login()
        this_user = login.get_login()
        code = ''
        element_lines = None
        rowct = 0
        server = TacticServerStub.get()

        type_codes = ['F', 'A', 'T', 'V']
        scales = ['1', '2', '3', 'FYI']
        in_safe = ['No', 'Yes']
        insrc = ['No', 'Yes', 'New', 'Approved', 'Fixed', 'Not Fixed', 'Approved by Production', 'Approved by Client',
                 'Approved as is']
        wo_code = str(my.kwargs.get('wo_code'))
        reloaded = False
        if 'reload' in my.kwargs.keys():
            if my.kwargs.get('reload') == 'true':
                reloaded = True
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code')
            element_lines = server.eval("@SOBJECT(twog/element_eval_lines['element_eval_code','%s']['@ORDER_BY','timecode_in asc'])" % code)
            elm_top = []
            elm_bottom = []
            for elm in element_lines:
                if elm.get('ordering') in [None,'']:
                    elm_bottom.append(elm)
                else:
                    elm_top.append(elm)
            from operator import itemgetter
            new_top = sorted(elm_top, key=itemgetter('ordering'))
            element_lines = []
            element_lines.extend(new_top)
            element_lines.extend(elm_bottom)
        if 'rowct' in my.kwargs.keys():
            rowct = int(my.kwargs.get('rowct'))
        linestbl = Table()
        linestbl.add_attr('class','linestbl')
        if rowct == 0 and not reloaded:
            linestbl.add_row()
            linestbl.add_cell("Timecode In")
            linestbl.add_cell("&nbsp;F")
            linestbl.add_cell("Description")
            linestbl.add_cell("In Safe")
            time_out_label = "Timecode Out"
            # Some clients want "Duration" instead
            duration_clients = ProdSetting.get_seq_by_key('qc_report_duration_clients')
            if my.kwargs.get('client_code') in duration_clients:
                time_out_label = "Duration"
            linestbl.add_cell(time_out_label)
            linestbl.add_cell("&nbsp;F")
            linestbl.add_cell("Code")
            linestbl.add_cell("Scale")
            linestbl.add_cell("Sector/Ch")
            linestbl.add_cell("In Source")
            plus_butt = linestbl.add_cell(" ")
        if code not in [None,''] and not reloaded:
            for el in element_lines:
                seen_descs = []
                if el.get('code') != '':
                    row = linestbl.add_row()
                    row.add_attr('line', rowct)
                    row.add_attr('code', el.get('code'))
                    row.add_attr('class', 'element_lines')

                    linestbl.add_cell(my.txtbox('timecode_in-%s' % rowct, el.get('timecode_in'), width='75px',
                                                js='yes'))
                    linestbl.add_cell('<input type="text" id="field_in-%s" name="field_in" value="%s" style="width: 20px;"/>' % (rowct, el.get('field_in')))

                    mm1 = linestbl.add_cell(my.txtbox('description-%s' % rowct, el.get('description'), width='450px',
                                                      js='no', style=el.get('description_style')))
                    insafe_select = SelectWdg('in_safe')
                    insafe_select.append_option('-', '')
                    for i in in_safe:
                        insafe_select.append_option(i, i)
                    insafe_select.set_value(el.get('in_safe'))
                    insafe_select.add_attr('id', 'in_safe-%s' % rowct)
                    mm2 = linestbl.add_cell(insafe_select)
                    mm2.add_attr('class', 'select_cell')

                    linestbl.add_cell(my.txtbox('timecode_out-%s' % rowct, el.get('timecode_out'), width='75px',
                                                js='yes'))
                    linestbl.add_cell('<input type="text" id="field_out-%s" name="field_out" value="%s" style="width: 20px;"/>' % (rowct, el.get('field_out')))
                    type_code_select = SelectWdg('type_code')
                    type_code_select.append_option('-', '')
                    for tc in type_codes:
                        type_code_select.append_option(tc, tc)
                    type_code_select.set_value(el.get('type_code'))
                    type_code_select.add_attr('id', 'type_code-%s' % rowct)
                    mm3 = linestbl.add_cell(type_code_select)
                    mm3.add_attr('class', 'select_cell')
                    scale_select = SelectWdg('scale')
                    scale_select.append_option('-', '')
                    for s in scales:
                        scale_select.append_option(s, s)
                    scale_select.set_value(el.get('scale'))
                    scale_select.add_attr('id', 'scale-%s' % rowct)
                    mm4 = linestbl.add_cell(scale_select)
                    mm4.add_attr('class', 'select_cell')

                    linestbl.add_cell(my.txtbox('sector_or_channel-%s' % rowct,el.get('sector_or_channel'),
                                                width='60px', js='no'))
                    insrc_select = SelectWdg('in_source')
                    insrc_select.append_option('-', '')
                    for i in insrc:
                        insrc_select.append_option(i, i)
                    insrc_select.set_value(el.get('in_source'))
                    insrc_select.add_attr('id', 'in_source-%s' % rowct)
                    mm5 = linestbl.add_cell(insrc_select)
                    mm5.add_attr('class', 'select_cell')
                    orderer = linestbl.add_cell(my.txtbox('ordering-%s' % rowct, el.get('ordering'), width='60px',
                                                          js='no'))
                    killer = linestbl.add_cell('<b>X</b>')  # This must delete the entry
                    killer.add_attr('id', 'killer-%s' % rowct)
                    killer.add_style('cursor: pointer;')
                    killer.add_behavior(my.get_kill_bvr(rowct, wo_code, el.get('code'), code))
                    rowct += 1

        erow = linestbl.add_row()
        erow.add_attr('line', rowct)
        erow.add_attr('code', '')
        erow.add_attr('class', 'element_lines')

        linestbl.add_cell(my.txtbox('timecode_in-%s' % rowct, '', width='75px', js='yes'))
        linestbl.add_cell('<input type="text" id="field_in-%s" name="field_in" value="" style="width: 20px;"/>' % (rowct))

        mm1 = linestbl.add_cell(my.txtbox('description-%s' % rowct, '', width='450px', js='no'))
        insafe_select = SelectWdg('in_safe')
        insafe_select.append_option('-', '')
        for i in in_safe:
            insafe_select.append_option(i, i)
        insafe_select.add_attr('id', 'in_safe-%s' % rowct)
        mm2 = linestbl.add_cell(insafe_select)
        mm2.add_attr('class', 'select_cell')

        linestbl.add_cell(my.txtbox('timecode_out-%s' % rowct, '', width='75px', js='yes'))
        linestbl.add_cell('<input type="text" id="field_out-%s" name="field_out" value="" style="width: 20px;"/>' % (rowct))
        type_code_select = SelectWdg('type_code')
        type_code_select.append_option('-', '')
        for tc in type_codes:
            type_code_select.append_option(tc,tc)
        type_code_select.add_attr('id', 'type_code-%s' % rowct)
        mm3 = linestbl.add_cell(type_code_select)
        mm3.add_attr('class', 'select_cell')
        scale_select = SelectWdg('scale')
        scale_select.append_option('-', '')
        for s in scales:
            scale_select.append_option(s, s)
        scale_select.add_attr('id', 'scale-%s' % rowct)
        mm4 = linestbl.add_cell(scale_select)
        mm4.add_attr('class', 'select_cell')

        linestbl.add_cell(my.txtbox('sector_or_channel-%s' % rowct, '', width='75px', js='no'))
        insrc_select = SelectWdg('in_source')
        insrc_select.append_option('-', '')
        for i in insrc:
            insrc_select.append_option(i, i)
        insrc_select.add_attr('id', 'in_source-%s' % rowct)
        mm5 = linestbl.add_cell(insrc_select)
        mm5.add_attr('class', 'select_cell')
        addnew = linestbl.add_cell('<b>+</b>')  # This must add new entry
        addnew.add_style('cursor: pointer;')
        addnew.add_behavior(my.get_add_line(rowct,wo_code, code))
        erow2 = linestbl.add_row()
        erow2.add_attr('class', 'new_element_line')

        return linestbl
