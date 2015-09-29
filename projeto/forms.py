# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from projeto.models import Timesheet, Os, TipoOs, Atividades, DotpDepartments
from django.db.models.fields import * 

from django.forms.fields import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
from django.db import models
from django.core.mail import send_mail

from django.forms.models import inlineformset_factory


class Periodo(forms.Form):
    data_inicio = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'vDateField', 'size':'10',}))
    data_final = forms.TextInput(attrs={'class':'vDateField', 'size':'10',})

class TimesheetModelForm(ModelForm):
    hora_inicio =  models.TimeField(db_column='horainicio')
    hora_final = models.TimeField(db_column='horafinal')
    cometarios = models.TextField()

    class Meta:
        model = Timesheet
        
        widgets = {
                   'hora_inicio': TextInput(attrs={'class': 'vTimeField', 'OnKeyUp':'javascript:Mascara_Hora(this);', 'size':'8', 'maxlength':'8'}),
                   'hora_final': TextInput(attrs={'class': 'vTimeField', 'OnKeyUp':'javascript:Mascara_Hora(this);', 'size':'8', 'maxlength':'8'}),
                   'horastrab': TextInput(attrs={'class': 'HiddenInput'}),
                  }

# ================================================================================================================

class FormOrdemServicoInternet(forms.ModelForm):
    
    class Meta:
        model = Os
        fields = ('author', 'ramal', 'maquina', 'email', 'dept_id', 'dept_id_filial','ticket_tipo_os','priority', 'subject',  'body', )
        widgets = {  
                     'author' : TextInput(attrs={'size':'40'}), 
                     'email'  : TextInput(attrs={'size':'75'}), 
                     'maquina' : TextInput(attrs={'size':'20'}), 
                     #'dept_id', 
                     #'ticket_tipo_os', 
                     'subject'  : TextInput(attrs={'size':'100'}),  
                     'body': Textarea(attrs={'cols': 110, 'rows': 10}),
                  }
        
    def __init__(self, *args, **kwargs):
        super(FormOrdemServicoInternet, self).__init__(*args, **kwargs)

        ppp = TipoOs.objects.exclude(parent=None).values_list('parent_id').query

        self.fields['ticket_tipo_os'] = forms.ModelChoiceField(queryset = TipoOs.objects.exclude(id__in=ppp).exclude(parent=None).exclude(intranet='N').order_by('parent','dsc_os') )
        self.fields['ticket_tipo_os'].label = u'Tipo de Solicitação'

        self.fields['dept_id'] = forms.ModelChoiceField(queryset = DotpDepartments.objects.filter(indica_filial = 0).exclude(dept_id = 2).order_by('dept_name'))
        self.fields['dept_id'].label = u'Departamento do Solicitante'
        self.fields['dept_id_filial'] = forms.ModelChoiceField(queryset = DotpDepartments.objects.filter(indica_filial = 1).order_by('dept_name'))
        self.fields['dept_id_filial'].label = u'Filial Solicitante'

    def enviar(self):        
        destino = 'suporte_ti@foreverliving.com.br' 
        email = self.cleaned_data['email']
        titulo = self.cleaned_data['subject'] 
        texto = u"""
                 Solicitante: %(author)s
                 E-mail: %(email)s
                 Departamento: %(dept_id)s
                 Tipo de Solicitação: %(ticket_tipo_os)s
                 Solicitação: %(subject)s  

                 Mensagem:
                 %(body)s
                 """ % self.cleaned_data 
        send_mail(subject=titulo, message=texto, from_email=destino, recipient_list=[email],)



# ================================================================================================================

class FormOS(forms.ModelForm):
    
    class Meta:
        model = Os
        fields = ('assignment', 'author', 'ramal', 'maquina', 'email', 'dept_id', 'dept_id_filial', 'ticket_tipo_os', 'priority', 'subject',   'body', 'ctype' )
        widgets = {  
                     'author' : TextInput(attrs={'size':'40'}), 
                     'email'  : TextInput(attrs={'size':'75'}), 
                     'maquina' : TextInput(attrs={'size':'20'}),
                     #'dept_id', 
                     #'ticket_tipo_os', 
                     'subject'  : TextInput(attrs={'size':'100'}),  
                     'body': Textarea(attrs={'cols': 110, 'rows': 10}),                     
                  }
        
    def __init__(self, *args, **kwargs):
        super(FormOS, self).__init__(*args, **kwargs)
        
        ppp = TipoOs.objects.exclude(parent=None).values_list('parent_id').query

        self.fields['ticket_tipo_os'] = forms.ModelChoiceField(queryset = TipoOs.objects.exclude(id__in=ppp).order_by('parent','dsc_os') )
        self.fields['ticket_tipo_os'].verbose_name = u'Tipo de Solicitação'
        #self.fields['assignment'].required = True 

# ================================================================================================================

