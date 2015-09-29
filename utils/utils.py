# -*- coding: utf-8 -*-
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import force_unicode


def troca_message(self, request, form, formsets):
     """
     Construct a change message from a changed object.
     """
     change_message = []
     if form.changed_data:
         #change_message.append(_('Changed %s.') % get_text_list(form.changed_data, _('and')))

         for name, field in form.fields.items():
             prefixed_name = form.add_prefix(name)
             data_value = field.widget.value_from_datadict(form.data, form.files, prefixed_name)
             initial_value = form.initial.get(name, field.initial)
             
             if field.widget._has_changed(initial_value,data_value):
                 change_message.append(_(' Alterado: %s: de:[ %s ] para:[ %s ] || \n') % (field.label,initial_value,data_value))
                
                 #if name == 'ins_operadora':
                 #    change_message.append(_(' Alterado: %s: de:[ %s ] para:[ %s ] || \n') % (field.label,Operadora.objects.get(pk=initial_value),Operadora.objects.get(pk=data_value)))
                 #elif name == 'ins_id_orgao' or name == 'uni_id_orgao':
                 #        change_message.append(_(' Alterado: %s: de:[ %s ] para:[ %s ] || \n') % (field.label,Orgao.objects.get(pk=initial_value),Orgao.objects.get(pk=data_value)))
                 #else:
                 #    change_message.append(_(' Alterado: %s: de:[ %s ] para:[ %s ] || \n') % (field.label,initial_value,data_value))
                

     change_message = ' '.join(change_message)

     return change_message or _('Sem campos alterados.')

