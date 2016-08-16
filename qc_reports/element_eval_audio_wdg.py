from tactic_client_lib import TacticServerStub
from tactic.ui.common import BaseRefreshWdg

from pyasm.web import Table
from pyasm.widget import TextWdg


class ElementEvalAudioWdg(BaseRefreshWdg):
    def init(my):
        my.content_pull = '<select REPLACE_ME><option value="">--Select--</option>'
        my.contents = ['5.1 Left', '5.1 Right', '5.1 Center', '5.1 LFE', '5.1 Left Surround', '5.1 Right Surround',
                       'Stereo Left', 'Stereo Right', 'Stereo Music Left', 'Stereo Music Right', 'Stereo FX Left',
                       'Stereo FX Right', 'Stereo M&E Left', 'Stereo M&E Right', 'Stereo Dialogue', 'Mono Narration',
                       'M.O.S', 'Mono', 'Mono Dialogue', 'Mono Music', 'Mono FX', 'Various']
        for c in my.contents:
            my.content_pull = '%s<option value="%s">%s</option>' % (my.content_pull, c, c)
        my.content_pull = '%s</select>' % my.content_pull

    def get_nums_only(my):
        behavior = {'css_class': 'clickme', 'type': 'keyup', 'cbjs_action': '''
                try{
                    var entered = bvr.src_el.value;
                    var old_val = bvr.src_el.getAttribute('old_val');
                    if(isNaN(entered)){
                        alert(entered + " is not a number. Please only enter numbers here.")
                        bvr.src_el.value = old_val;
                    }else{
                        bvr.src_el.setAttribute('old_val',entered);
                    }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def selbox(my, name, val, code, old_val, width='200px'):
        fresh = my.content_pull
        build_str = 'id="%s" code="%s" old_val="%s" width="%s"' % (name, code, old_val, width)
        fresh = fresh.replace('REPLACE_ME',build_str)
        selected_str = 'value="%s"' % val
        if selected_str in fresh:
            fresh = fresh.replace(selected_str, '%s selected="selected"' % selected_str)
        else:
            fresh = fresh.replace('</select>', '<option value="%s" selected="selected">%s</option></select>' % (val, val))
        return fresh

    def txtbox(my, name, val, code, old_val, width='200px', js='no'):
        txt = TextWdg(name)
        txt.add_attr('id', name)
        txt.add_attr('code', code)
        txt.add_attr('old_val', old_val)
        txt.add_style('width: %s;' % width)
        txt.set_value(val)
        if js == 'yes':
            txt.add_behavior(my.get_nums_only())
        return txt

    def get_display(my):
        element_auds = []
        server = TacticServerStub.get()
        wo_code = str(my.kwargs.get('wo_code'))
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code')
            element_auds = server.eval("@SOBJECT(twog/element_eval_audio['element_eval_code','%s']['@ORDER_BY','channel'])" % code)
        force_it = False
        if 'force_it' in my.kwargs.keys():
            if my.kwargs.get('force_it') == 'true':
                force_it = True
        channels = 21
        if 'channels' in my.kwargs.keys():
            channels = int(my.kwargs.get('channels'))
        if len(element_auds) > 0 and not force_it:
            channels = len(element_auds)
        leng = len(element_auds)
        for i in range(leng, channels - leng):
            element_auds.append(None)
        a_third = int(channels/3)
        if int(float(float(float(channels)/float(3))*1000)) != a_third * 1000:
            a_third += 1
        grand_table = Table()
        grand_table.add_attr('id', 'audio_information')
        grand_table.add_attr('channels', channels)
        grand_table.add_row()
        atable = None
        for i in range(0,channels):
            if i in [0,a_third,(a_third * 2)]:
                atable = Table()
                atable.add_attr('class','atable')
                atable.add_attr('border','1')
                atable.add_row()
                atable.add_cell('Channel')
                atable.add_cell('Content')
                atable.add_cell('Tone')
                atable.add_cell('Peak')
            atable.add_row()
            the_code = ''
            channel = ''
            content = ''
            tone = ''
            peak = ''
            if i < len(element_auds):
                if element_auds[i] != None:
                    the_code = element_auds[i].get('code')
                    channel = element_auds[i].get('channel')
                    content = element_auds[i].get('content')
                    tone = element_auds[i].get('tone')
                    peak = element_auds[i].get('peak')
            atable.add_cell(my.txtbox('channel-%s' % i,channel,the_code,channel,width='68px',js='yes'))
            sellie = atable.add_cell(my.txtbox('content-%s' % i,content,the_code,content,width='132px'))
            atable.add_cell(my.txtbox('tone-%s' % i,tone,the_code,tone,width='68px'))
            atable.add_cell(my.txtbox('peak-%s' % i,peak,the_code,peak,width='68px'))
            if i in [a_third-1,(a_third*2)-1,channels-1]:
                grand_cell = grand_table.add_cell(atable)
                grand_cell.add_attr('valign','top')
                if i != channels-1:
                    grand_table.add_cell('&nbsp;')
                atable = None
        return grand_table
