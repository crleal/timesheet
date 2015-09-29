# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from smart_selects.db_fields import ChainedForeignKey 
from datetime import datetime
from datetime import date
from decimal import *
from django.core.mail import send_mail

from django.core.validators import *

import string

from math import trunc

from django.contrib.auth.models import User

class DotpCompanies(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_module = models.IntegerField()
    company_name = models.CharField(max_length=100, blank=True)
    company_phone1 = models.CharField(max_length=30, blank=True)
    company_phone2 = models.CharField(max_length=30, blank=True)
    company_fax = models.CharField(max_length=30, blank=True)
    company_address1 = models.CharField(max_length=50, blank=True)
    company_address2 = models.CharField(max_length=50, blank=True)
    company_city = models.CharField(max_length=30, blank=True)
    company_state = models.CharField(max_length=30, blank=True)
    company_zip = models.CharField(max_length=11, blank=True)
    company_primary_url = models.CharField(max_length=255, blank=True)
    company_owner = models.IntegerField()
    company_description = models.TextField(blank=True)
    company_type = models.IntegerField()
    company_email = models.CharField(max_length=255, blank=True)
    company_custom = models.TextField(blank=True)
    class Meta:
        db_table = u'dotp_companies'
        verbose_name = u'Compania'

    def __unicode__(self):
        return self.company_name

# ================================================================================================================

class DotpUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_contact = models.IntegerField()
    user_username = models.CharField(max_length=255)
    user_password = models.CharField(max_length=32)
    user_parent = models.IntegerField()
    user_type = models.IntegerField()
    user_company = models.IntegerField(null=True, blank=True)
    user_department = models.IntegerField(null=True, blank=True)
    user_owner = models.IntegerField()
    user_signature = models.TextField(blank=True)
    class Meta:
        db_table = u'dotp_users'

    def __unicode__(self):
        return u'%s' % (self.user_username)

    def get_timesheet(self):
       return self.timesheet_set.all()

    def get_timesheet_horas(self):
       return self.timesheet_set.values('usuario', 'data').annotate(horas=Sum('horastrab')).order_by('-data') 

    def pega_registros(self):
       tt = Timesheet.objects.raw('SELECT id, username, data, dia_semana, horas, comentario,  descricao from ('+
                                  'SELECT time.id, dt.username, dt.data, dt.dia_semana, round( sum(horastrab), 1 ) horas, dt.comentario,  dt.descricao '+
                                  'FROM timesheet time '+
                                  '         RIGHT JOIN (select dias.id, dias.username, dias.data, dias.dia_semana, dias.qtd_horas, dias.comentario,  ferias.descricao  '+
                                  '                     from   '+
                                  '                        (SELECT id, username, dt.data, dt.dia_semana, dt.qtd_horas, dt.comentario,  "" descricao  '+
                                  '                         FROM auth_user, timesheet_data dt  '+
                                  '                         WHERE dt.data <= now()) dias  '+
                                  '                        left join  '+
                                  '                         (SELECT dt1.id, dt1.username, dt1.data, dt1.dia_semana, 0 qtd_horas, "" comentario, tf.descricao '+
                                  '                          FROM (SELECT id, username, dt.data, dt.dia_semana, dt.qtd_horas, dt.comentario, "" descricao '+
                                  '                                FROM auth_user, timesheet_data dt '+
                                  '                                WHERE dt.data <= now( ) ) dt1, timesheet_ferias tf '+
                                  '                          WHERE dt1.id = tf.usuario '+
                                  '                            AND dt1.data   BETWEEN tf.datainicio  AND tf.datafim) ferias on (dias.id = ferias.id and dias.data = ferias.data) '+
                                  '                    ) dt ON ( time.data = dt.data AND time.usuario = dt.id ) , '+ 
                                  '                    (SELECT usuario FROM timesheet GROUP BY usuario ) usu '+ 
                                  'WHERE (usu.usuario = dt.id) '+
                                  'GROUP BY dt.username, dt.data, dt.dia_semana, dt.comentario,  dt.descricao '+
                                  'ORDER BY  data desc) as BLABLA')
       return tt   

# ================================================================================================================

class DotpContacts(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_first_name = models.CharField(max_length=30, blank=True)
    contact_last_name = models.CharField(max_length=30, blank=True)
    contact_order_by = models.CharField(max_length=30)
    contact_title = models.CharField(max_length=50, blank=True)
    contact_birthday = models.DateField(null=True, blank=True)
    contact_job = models.CharField(max_length=255, blank=True)
    contact_company = models.CharField(max_length=100)
    contact_department = models.TextField(blank=True)
    contact_type = models.CharField(max_length=20, blank=True)
    contact_email = models.CharField(max_length=255, blank=True)
    contact_email2 = models.CharField(max_length=255, blank=True)
    contact_url = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_phone2 = models.CharField(max_length=30, blank=True)
    contact_fax = models.CharField(max_length=30, blank=True)
    contact_mobile = models.CharField(max_length=30, blank=True)
    contact_address1 = models.CharField(max_length=60, blank=True)
    contact_address2 = models.CharField(max_length=60, blank=True)
    contact_city = models.CharField(max_length=30, blank=True)
    contact_state = models.CharField(max_length=30, blank=True)
    contact_zip = models.CharField(max_length=11, blank=True)
    contact_country = models.CharField(max_length=30, blank=True)
    contact_jabber = models.CharField(max_length=255, blank=True)
    contact_icq = models.CharField(max_length=20, blank=True)
    contact_msn = models.CharField(max_length=255, blank=True)
    contact_yahoo = models.CharField(max_length=255, blank=True)
    contact_aol = models.CharField(max_length=30, blank=True)
    contact_notes = models.TextField(blank=True)
    contact_project = models.IntegerField()
    contact_icon = models.CharField(max_length=20, blank=True)
    contact_owner = models.IntegerField(null=True, blank=True)
    contact_private = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dotp_contacts'
        verbose_name = u'contato'

    def __unicode__(self):
        return self.contact_first_name

# ================================================================================================================

class DotpDepartments(models.Model):
    dept_id = models.AutoField(primary_key=True, db_column='dept_id')
    dept_parent = models.IntegerField()
    dept_company = models.IntegerField()
    dept_name = models.TextField()
    dept_phone = models.CharField(max_length=30, blank=True)
    dept_fax = models.CharField(max_length=30, blank=True)
    dept_address1 = models.CharField(max_length=30, blank=True)
    dept_address2 = models.CharField(max_length=30, blank=True)
    dept_city = models.CharField(max_length=30, blank=True)
    dept_state = models.CharField(max_length=30, blank=True)
    dept_zip = models.CharField(max_length=11, blank=True)
    dept_url = models.CharField(max_length=25, blank=True)
    dept_desc = models.TextField(blank=True)
    dept_owner = models.IntegerField()
    indica_filial = models.IntegerField(default=0)
    class Meta:
        db_table = u'dotp_departments'
        verbose_name = u'departamento'

    def __unicode__(self):
        return self.dept_name

# ================================================================================================================

# dotp_projects  Query para calculo percent_complete do projeto
#select 
# SUM(t1.task_duration * t1.task_percent_complete * IF(t1.task_duration_type = 24, 8, t1.task_duration_type)) / 
#                                                                    SUM(t1.task_duration * IF(t1.task_duration_type = 24, 8, t1.task_duration_type)) 
#   AS project_percent_complete
#from  dotp_projects  p, dotp_tasks t1
#where p.project_id = t1.task_project
#   and project_id = 198
#   AND t1.task_id = t1.task_parent


# ================================================================================================================

class DotpProjects(models.Model):
    project_id = models.AutoField(primary_key=True, db_column='project_id')
    project_company = models.IntegerField()
    project_company_internal = models.IntegerField()
    project_department = models.IntegerField()
    project_name = models.CharField(max_length=255, blank=True)
    project_short_name = models.CharField(max_length=30, blank=True)
    project_owner = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='project_owner')    # IntegerField(null=True, blank=True)
    project_url = models.CharField(max_length=255, blank=True)
    project_demo_url = models.CharField(max_length=255, blank=True)
    project_start_date = models.DateTimeField(null=True, blank=True)
    project_end_date = models.DateTimeField(null=True, blank=True)
    project_status = models.IntegerField(null=True, blank=True)
    project_percent_complete = models.IntegerField(null=True, blank=True)
    project_color_identifier = models.CharField(max_length=6, blank=True)
    project_description = models.TextField(blank=True)
    project_target_budget = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    project_actual_budget = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    project_creator = models.IntegerField(null=True, blank=True)
    project_private = models.IntegerField(null=True, blank=True)
    project_departments = models.ForeignKey(DotpDepartments, verbose_name=u'Departamento', db_column='project_departments') 
    project_contacts = models.CharField(max_length=100, blank=True)
    project_priority = models.IntegerField(null=True, blank=True)
    project_type = models.IntegerField()
   
    class Meta:
        db_table = u'dotp_projects'
        verbose_name = u'Projeto'
        ordering = ['project_name']

    def __unicode__(self):
        return self.project_name

# ================================================================================================================

class DotpProjectContacts(models.Model):
    project_id = models.ForeignKey(DotpProjects, verbose_name=u'Projetos', db_column='project_id',primary_key=True,)
    contact_id = models.ForeignKey(DotpContacts, verbose_name=u'Contatos', db_column='contact_id',primary_key=True,)

    class Meta:
        db_table = u'dotp_project_contacts'
        verbose_name = u'Contatos do Projeto'

    def __unicode__(self):
        return self.contact_id.contact_first_name

# ================================================================================================================

class DotpProjectDepartments(models.Model):
    project_id = models.ForeignKey(DotpProjects, verbose_name=u'Projetos', db_column='project_id',primary_key=True,)
    department_id = models.ForeignKey(DotpDepartments, verbose_name=u'Departamento', db_column='department_id', primary_key=True,)

    class Meta:
        db_table = u'dotp_project_departments'

# ================================================================================================================

class DotpProjectDesignerOptions(models.Model):
    pd_option_id = models.AutoField(primary_key=True)
    pd_option_user = models.IntegerField(unique=True)
    pd_option_view_project = models.IntegerField()
    pd_option_view_gantt = models.IntegerField()
    pd_option_view_tasks = models.IntegerField()
    pd_option_view_actions = models.IntegerField()
    pd_option_view_addtasks = models.IntegerField()
    pd_option_view_files = models.IntegerField()
    class Meta:
        db_table = u'dotp_project_designer_options'

# tasks # ================================================================================================================

class Atividades(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255, blank=True)
    task_parent = models.ForeignKey('self', null=True, blank=True, db_column='task_parent') #models.ForeignKey('self', verbose_name=u'Atividade Pai', related_name='child', , null=True, blank=True, )
    task_milestone = models.IntegerField(null=True, blank=True)
    task_project = models.ForeignKey(DotpProjects, verbose_name=u'Projeto', db_column='task_project') 
    task_owner = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='task_owner')    # IntegerField(null=True, blank=True)
    task_start_date = models.DateTimeField(null=True, blank=True)
    task_duration = models.FloatField(null=True, blank=True)
    task_duration_type = models.IntegerField()
    task_hours_worked = models.FloatField(null=True, blank=True)
    task_end_date = models.DateTimeField(null=True, blank=True)
    task_status = models.IntegerField(null=True, blank=True)
    task_priority = models.IntegerField(null=True, blank=True)
    task_percent_complete = models.IntegerField(null=True, blank=True)
    task_description = models.TextField(blank=True)
    task_target_budget = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    task_related_url = models.CharField(max_length=255, blank=True)
    task_creator = models.IntegerField()
    task_order = models.IntegerField()
    task_client_publish = models.IntegerField()
    task_dynamic = models.IntegerField()
    task_access = models.IntegerField()
    task_notify = models.IntegerField()
    task_departments = models.CharField(max_length=100, blank=True)
    task_contacts = models.CharField(max_length=100, blank=True)
    task_custom = models.TextField(blank=True)
    task_type = models.IntegerField()
    class Meta:
        db_table = u'dotp_tasks'
        verbose_name = u'Atividade'

#    def __unicode__(self):
#        return u'%s - %s - Completado: %s %s' % (self.task_name, self.task_project, self.task_percent_complete, '%')
 
    def future_data(self):
      if self.task_end_date > datetime.now():
         return True
      return False    

    def tem_pai(self):
         if self.task_parent.task_id == self.task_id:
            return False
         return True

    def __unicode__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.task_name )
        return u'%s - %s - %s -> %s' % (self.task_id, self.task_percent_complete, self.task_project , self.get_separator().join(p_list)) #, self.task_percent_complete, '%')

        
    def __str__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.task_name.encode('iso-8859-1','replace') )
        return self.get_separator().join(p_list)

    def get_familia(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.task_name.encode('iso-8859-1','replace') )
        return self.get_separator().join(p_list)
    
        
    def get_absolute_url(self):
        if self.parent_id:
            return "/tag/%s/%s/" % (self.task_parent.task_name, self.task_name)
        else:
            return "/tag/%s/" % (self.task_name)
        
    def _recurse_for_parents(self, cat_obj):
         p_list = []

         if cat_obj.tem_pai():
               p = cat_obj.task_parent
               p_list.append(p.task_name)
               more = self._recurse_for_parents(p)
               p_list.extend(more)
         if cat_obj == self and p_list:
            p_list.reverse()
         return p_list
                
    def get_separator(self):
         return ' :: '
        
    def _parents_repr(self):
         p_list = self._recurse_for_parents(self)
         return self.get_separator().join(p_list)
    _parents_repr.short_description = "Tag parents"

# ================================================================================================================ 

class DotpUserTasks(models.Model):
    user_id = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='user_id', primary_key=True)
    user_type = models.IntegerField()
    task_id = models.ForeignKey(Atividades, db_column='task_id', verbose_name='Atividade', primary_key=True)
    perc_assignment = models.IntegerField()
    user_task_priority = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dotp_user_tasks'

    def __unicode__(self):
        return u'%s' % (self.task_id)
 
# ================================================================================================================ 
 
class DotpTaskContacts(models.Model):
    task_id = models.ForeignKey(Atividades, verbose_name=u'Atividades', db_column='task_id',primary_key=True,)
    contact_id = models.ForeignKey(DotpContacts, verbose_name=u'Contatos', db_column='contact_id',primary_key=True,)

    class Meta:
        db_table = u'dotp_task_contacts'
        verbose_name = u'Contatos da Atividade' 

    def __unicode__(self):
        return self.contact_id.contact_first_name

# ================================================================================================================

class DotpTaskDepartments(models.Model):
    task_id = models.ForeignKey(Atividades, verbose_name=u'Atividades', db_column='task_id',primary_key=True,)
    department_id = models.ForeignKey(DotpDepartments, verbose_name=u'Departamento', db_column='department_id', primary_key=True,)

    class Meta:
        db_table = u'dotp_task_departments'

# ================================================================================================================

#class DotpTaskDependencies(models.Model):
#    dependencies_task_id = models.ForeignKey(Atividades, verbose_name=u'Atividades', db_column='dependencies_task_id',primary_key=True,)
#    dependencies_req_task_id = models.ForeignKey(Atividades, verbose_name=u'Atividades', db_column='dependencies_req_task_id',primary_key=True,)
#    class Meta:
#        db_table = u'dotp_task_dependencies'


# ================================================================================================================
#  REgistro de Atividades
#
class DotpTaskLog(models.Model):
    task_log_id = models.AutoField(primary_key=True)
    task_log_task = models.ForeignKey(Atividades, db_column='task_log_task', verbose_name='Atividade', null=True, blank=True,)
    task_log_name = models.CharField(max_length=255, blank=True)
    task_log_description = models.TextField(blank=True)
    task_log_creator = models.IntegerField()
    task_log_hours = models.FloatField()
    task_log_date = models.DateTimeField(null=True, blank=True, default= datetime.now())
    task_log_costcode = models.CharField(max_length=8)
    task_log_problem = models.IntegerField(null=True, blank=True)
    task_log_reference = models.IntegerField(null=True, blank=True)
    task_log_related_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'dotp_task_log'

# ================================================================================================================

class TipoOs(models.Model):
     id =  models.AutoField(primary_key=True)
     dsc_os = models.CharField(max_length=20, verbose_name=u'Tipo OS')
     parent = models.ForeignKey('self', blank=True, null=True, related_name='child') 
     dsc_os_volpe = models.CharField(max_length=2, verbose_name=u'Código Tipo OS Volpe', blank=True, null=True)
     intranet = models.CharField(max_length=1, verbose_name=u'Intranet', default='S') 
     class Meta:
        db_table = u'tipo_os' 
    
     def __unicode__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.dsc_os)
        return u'%s' % (self.get_separator().join(p_list))

#        return u'%s %s' % (self.dsc_os, self._parents_repr )

     class Admin:
        list_display = ('dsc_os', '_parents_repr')
        
     def __str__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.dsc_os)
        return self.get_separator().join(p_list)

   
     def get_absolute_url(self):
        if self.parent_id:
            return "/tag/%s/%s/" % (self.parent.dsc_os, self.dsc_os)
        else:
            return "/tag/%s/" % (self.dsc_os)
        
     def _recurse_for_parents(self, cat_obj):
         p_list = []
         if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.dsc_os)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
         if cat_obj == self and p_list:
            p_list.reverse()
         return p_list
                
     def get_separator(self):
         return ' :: '
        
     def _parents_repr(self):
         p_list = self._recurse_for_parents(self)
         return self.get_separator().join(p_list)
     _parents_repr.short_description = "Tag parents"
        
     def get_timesheet_horas(self):
       return self.Os_set.values('ticket_tipo_os', 'data').annotate(horas=Sum('horastrab')).order_by('data') 

# ================================================================================================================
        
PRIORITY_CHOICES = ((0,'Baixa'),(1,'Normal'),(2,'Alta'),(3,'A Mais Alta'),(4,'Emergencia'))                

TYPE_CHOICES = (("Open", "Aberto"), ("Processing", "Em processamento"), ("Closed", "Encerrados"), ("Deleted", "Removido(s)"),  ("standby", "Em espera"))

class Os(models.Model):
    ticket = models.AutoField(primary_key=True)

    ticket_company = models.ForeignKey(DotpCompanies, verbose_name=u'Empresa', db_column='ticket_company', default = 1)    
    author = models.CharField(u'Solicitante', max_length=100)
    ramal = models.CharField(u'Ramal', db_column= 'ramal', max_length=20, )
    maquina = models.CharField(u'Número da Máquina', db_column= 'maquina', max_length=15,)
    email = models.EmailField(u'E-mail Solicitante', db_column= 'email', max_length=75)
    dept_id = models.ForeignKey(DotpDepartments, verbose_name = u'Dep Solicitante', related_name='departamento',
                            db_column='dept_id', limit_choices_to={'indica_filial': 0}) 
    dept_id_filial = models.ForeignKey(DotpDepartments, verbose_name = u'Filial Solicitante', related_name='filial',
                            db_column='dept_id_filial', limit_choices_to={'indica_filial': 1},  ) 
    ticket_tipo_os = models.ForeignKey(TipoOs, verbose_name=u'Tipo de Solicitação', db_column='ticket_tipo_os')
    ticket_project = models.ForeignKey(DotpProjects, verbose_name=u'Projeto', db_column='ticket_project', null=True, blank=True,) 
    subject = models.CharField(u'Solicitação', max_length=100)
    body = models.TextField(u'Comentários')
    ctype = models.CharField(max_length=15, verbose_name=u'Situação', db_column='type', choices=TYPE_CHOICES, default = "Open")
    assignment = models.ForeignKey(User, verbose_name=u'Usuário', db_column='assignment', null=True, blank=True,) 
    priority = models.IntegerField('Prioridade', choices=PRIORITY_CHOICES, default = 1)
    #cc = models.CharField(max_length=255)
    #recipient = models.CharField(max_length=100)
    #signature = models.TextField(blank=True)
    #attachment = models.IntegerField()
    #timestamp = models.IntegerField(null=True, blank=True,)
    #parent = models.IntegerField()
    #activity = models.IntegerField()
    data = models.DateTimeField(default=datetime.now(), )
    end_ip = models.CharField(u'IP Criação', db_column= 'end_ip', max_length=20,)
    mandar_email = models.CharField(u'Enviar E-mail', db_column= 'mandar_email', max_length=1,)
    #arquivos = models.ManyToManyField(Os_arquivos, through='Os_arquivos', null=True, blank=True)
    
    
    class Meta:
        db_table = u'dotp_tickets'
        verbose_name=u'Ordem de Serviço'

    def usuario_(self):
        return  self.assignment

    def tipo(self):
        return self.ticket_tipo_os

    def situacao(self):
        return self.get_ctype_display()

    def prioridade(self):
        return self.get_priority_display()


    def data_(self):
        return self.data.strftime('%d/%m/%Y %H:%M')

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.ticket, self.subject, self.author, self.ctype)

    def get_timesheet_horas(self):
       return self.timesheet_set.values('ticket__ticket_tipo_os', 'data').annotate(horas=Sum('horastrab')).order_by('-data') 


   # def save(self, *args, **kwargs):
       # if self.ticket:
       #    osaux = Os.objects.get(pk=self.ticket)
       #    if osaux.assignment:
       #       userosaux = DotpUserOS.objects.filter(user_id = osaux.assignment, ticket=osaux )    
       #       userosaux.delete()
        # 
       # if self.assignment:
       #    userosaux = DotpUserOS.objects.filter(user_id = self.assignment, ticket=self )
       #    if not userosaux:
       #       DotpUserOS.objects.create(user_id = self.assignment, ticket=self )
        #
    #    super(Os, self).save(*args, **kwargs)


class Os_arquivos(models.Model):
    ticket  = models.ForeignKey(Os, verbose_name=u'Ordel de Serviço', db_column='ticket',)
    arquivo = models.FileField(upload_to='arquivos_os')
    class Meta:
        db_table = u'os_arquivo'
        verbose_name=u'Arquivos Ordem de Serviço'
        

class DotpUserOS(models.Model):
    user_id = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='user_id', )
    ticket  = models.ForeignKey(Os, verbose_name=u'Ordem de Serviço', db_column='ticket',)
    class Meta:
        db_table = u'os_user'

    def __unicode__(self):
        return u'%s' % (self.ticket)


# ================================================================================================================

class Timesheet(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='usuario',) 
    ticket = models.ForeignKey(Os, db_column='ticket', verbose_name= 'Ordem de Serviço', null=True, blank=True,)
    task_id = models.ForeignKey(Atividades, db_column='task_id', verbose_name='Atividade', null=True, blank=True,)
    percent_complete = models.IntegerField(null=True, blank=True, verbose_name = '% Concluido Atividade', )
    data =  models.DateField( db_column='data', max_length=10)
    hora_inicio =  models.TimeField(db_column='horainicio',max_length=8)
    hora_final = models.TimeField(db_column='horafinal', max_length=8)
    cometarios = models.TextField(u'Comentários')
    horastrab = models.FloatField(null=True, blank=True,)  
    trabsobreaviso = models.BooleanField(verbose_name=u"Trabalho Sobre Aviso")
  

    class Meta:
        db_table = u'timesheet'

    def __unicode__(self):
        return u'%s %s %s' % (self.data.strftime('%d/%m/%Y'), self.hora_inicio, self.usuario )

    def usuario_(self):
        return  self.usuario

    #def atividades_(self):
    #    return self.task_id

    def os(self):
        return self.ticket

    os.admin_order_field  = 'ticket'
    os.allow_tags = True
    os.label_tag= u'Ordem de Serviço'

    def atividade(self):
        return self.task_id

    atividade.admin_order_field  = 'task_id'

    def data_(self):
        return self.data.strftime('%d/%m/%Y')

    data_.admin_order_field = 'data'

    def get_timesheet(self, usu):
        return self.filter(usuario=usu)

    def tempo_trab(self):
        return round(( ((self.hora_final.hour * 60) + self.hora_final.minute)  - ((self.hora_inicio.hour * 60) + self.hora_inicio.minute) ) /60.0 , 1)
  
    tempo_trab.admin_order_field = 'horastrab' 


    def clean(self):
 
        if self.ticket is None:
            if self.task_id is None:
               raise ValidationError('Escolha a Ordem de Serviço ou a Atividade!!') 
        
        timesheetConfig = TimesheetConfig.objects.all()  
        dias = timesheetConfig[0].dias
        
        hoje = date.today() 
        delta = hoje - self.data
        #r = delta.days if (delta.days > 0) else "erro"

        if delta.days > dias:
           raise ValidationError('Data inválida, periodo já bloqueado!!')

        #if Timesheet.objects.filter( data=self.data, hora_final__gt=self.hora_inicio, usuario = self.usuario ).count() > 0:
        #   raise ValidationError('Hora Inicial inválida, já existe dentro de um periodo já preenchido!!')
        if self.id:
           if Timesheet.objects.filter( data=self.data, hora_inicio__lt=self.hora_inicio, hora_final__gt=self.hora_inicio, usuario = self.usuario ).exclude(id=self.id).count() > 0:
              raise ValidationError('Hora Inicial inválida, já existe dentro de um periodo já preenchido!!')
           elif Timesheet.objects.filter( data=self.data, hora_inicio__lt=self.hora_final, hora_final__gt=self.hora_final, usuario = self.usuario ).exclude(id=self.id).count() > 0:
              raise ValidationError('Hora final inválida, já existe dentro de um periodo já preenchido!!')
        else:  
           if Timesheet.objects.filter( data=self.data, hora_inicio__lt=self.hora_inicio, hora_final__gt=self.hora_inicio, usuario = self.usuario ).count() > 0:
              raise ValidationError('Hora Inicial inválida, já existe dentro de um periodo já preenchido!!')
           elif Timesheet.objects.filter( data=self.data, hora_inicio__lt=self.hora_final, hora_final__gt=self.hora_final, usuario = self.usuario ).count() > 0:
              raise ValidationError('Hora final inválida, já existe dentro de um periodo já preenchido!!')
    
        if self.hora_final <  self.hora_inicio:
           raise ValidationError('Hora Final maior que Hora Inicio')

    def save(self, *args, **kwargs):
        if self.task_id:
            diftime =  ( ((self.hora_final.hour * 60) + self.hora_final.minute)  - ((self.hora_inicio.hour * 60) + self.hora_inicio.minute) ) /60.0
            tasklog = DotpTaskLog.objects.create(task_log_task = self.task_id, task_log_name = self.task_id.task_name, task_log_description = self.cometarios,
                            task_log_creator = self.usuario.user_id, task_log_hours = round(diftime, 1) )
            tasklog.save()
            if self.percent_complete:
               task = Atividades.objects.get(task_id=self.task_id.task_id)
               if self.percent_complete > task.task_percent_complete:
                  percdiff = self.percent_complete - task.task_percent_complete
                  task.task_percent_complete = self.percent_complete          
                  task.save()
        else:
           if self.ticket:
              if self.percent_complete:
                 if self.percent_complete == 100:
                    #ticket = Os.objects.get(ticket=self.ticket)
                    self.ticket.ctype = 'Closed'
                    self.ticket.save()
                    if  self.ticket.mandar_email == 'S':
                        contato = DotpContacts.objects.get(contact_id=self.usuario.user_id)
                        origem_email = 'suporte_ti@foreverliving.com.br' 
                        email = self.ticket.email
                        titulo = self.ticket.subject
                        texto = u"""
O atendimento da solicitação de número: %s foi concluido.
                  
Solicitante: %s
E-mail: %s
Departamento: %s
Tipo de Solicitação: %s
Solicitação: %s  
 
Mensagem:
%s

Comentário do Analista de TI:
%s  
                                  """ % (self.ticket.ticket, self.ticket.author, self.ticket.email, self.ticket.dept_id, self.ticket.ticket_tipo_os, 
                                         self.ticket.subject, self.ticket.body, self.cometarios )
                        send_mail(subject=titulo, message=texto, from_email=origem_email, recipient_list=[email, contato.contact_email ],) 
                          

        diftime =  round(( ((self.hora_final.hour * 60) + self.hora_final.minute)  - ((self.hora_inicio.hour * 60) + self.hora_inicio.minute) ) /60.0 , 1)
        self.horastrab = diftime
        super(Timesheet, self).save(*args, **kwargs)


class TimesheetConsulta(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='usuario',) 
    ticket = models.ForeignKey(Os, db_column='ticket', verbose_name= 'Ordem de Serviço', null=True, blank=True,)
    task_id = models.ForeignKey(Atividades, db_column='task_id', verbose_name='Atividade', null=True, blank=True,)
    percent_complete = models.IntegerField(null=True, blank=True, verbose_name = '% Concluido Atividade', )
    data =  models.DateField( db_column='data', max_length=10)
    hora_inicio =  models.TimeField(db_column='horainicio',max_length=8)
    hora_final = models.TimeField(db_column='horafinal', max_length=8)
    cometarios = models.TextField(u'Comentários')
    horastrab = models.FloatField(null=True, blank=True,)  
    trabsobreaviso = models.BooleanField(verbose_name=u"Trabalho Sobre Aviso")
  
    class Meta:
        db_table = u'timesheet'
        
# ================================================================================================================   

class DotpHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_user = models.IntegerField()
    history_action = models.CharField(max_length=20)
    history_item = models.IntegerField()
    history_table = models.CharField(max_length=20)
    history_project = models.IntegerField()
    history_name = models.CharField(max_length=255, blank=True)
    history_changes = models.TextField(blank=True)
    history_description = models.TextField(blank=True)
    class Meta:
        db_table = u'dotp_history'

# ================================================================================================================

class DotpInvoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_project = models.IntegerField()
    invoice_status = models.IntegerField()
    invoice_date = models.IntegerField()
    invoice_paid = models.IntegerField(null=True, blank=True)
    invoice_creator = models.IntegerField()
    invoice_contact = models.CharField(max_length=765)
    invoice_notes = models.TextField()
    class Meta:
        db_table = u'dotp_invoice'

# ================================================================================================================

class DotpInvoiceCompany(models.Model):
    invoice_company = models.IntegerField()
    invoice_email = models.CharField(max_length=150)
    invoice_email_name = models.CharField(max_length=150)
    invoice_name = models.CharField(max_length=150)
    invoice_sendemail = models.IntegerField()
    invoice_recur = models.IntegerField()
    invoice_sentdate = models.DateField()
    class Meta:
        db_table = u'dotp_invoice_company'

# ================================================================================================================

class DotpInvoiceCompanyItems(models.Model):
    company = models.IntegerField()
    item = models.CharField(max_length=765)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table = u'dotp_invoice_company_items'

# ================================================================================================================

class DotpInvoiceTaskQueue(models.Model):
    task_queue_id = models.AutoField(primary_key=True)
    task_invoice = models.IntegerField()
    task_amount = models.FloatField()
    task_log_id = models.BigIntegerField()
    item_description = models.TextField(blank=True)
    class Meta:
        db_table = u'dotp_invoice_task_queue'

# ================================================================================================================

class DotpLinks(models.Model):
    link_id = models.AutoField(primary_key=True)
    link_url = models.CharField(max_length=765)
    link_project = models.IntegerField()
    link_task = models.IntegerField()
    link_name = models.CharField(max_length=765)
    link_parent = models.IntegerField(null=True, blank=True)
    link_description = models.TextField(blank=True)
    link_owner = models.IntegerField(null=True, blank=True)
    link_date = models.DateTimeField(null=True, blank=True)
    link_icon = models.CharField(max_length=60, blank=True)
    link_category = models.IntegerField()
    class Meta:
        db_table = u'dotp_links'

# ================================================================================================================

class DotpPermissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_user = models.IntegerField()
    permission_grant_on = models.CharField(unique=True, max_length=36)
    permission_item = models.IntegerField(unique=True)
    permission_value = models.IntegerField()
    class Meta:
        db_table = u'dotp_permissions'

# ================================================================================================================

class DotpUserAccessLog(models.Model):
    user_access_log_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    user_ip = models.CharField(max_length=45)
    date_time_in = models.DateTimeField(null=True, blank=True)
    date_time_out = models.DateTimeField(null=True, blank=True)
    date_time_last_action = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'dotp_user_access_log'

# ================================================================================================================

class DotpUserEvents(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    class Meta:
        db_table = u'dotp_user_events'

# ================================================================================================================

class DotpUserPreferences(models.Model):
    pref_user = models.CharField(max_length=36)
    pref_name = models.CharField(max_length=216)
    pref_value = models.CharField(max_length=96)
    class Meta:
        db_table = u'dotp_user_preferences'

# ================================================================================================================

class DotpUserRoles(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    class Meta:
        db_table = u'dotp_user_roles'

# ================================================================================================================

class DotpUserTaskPin(models.Model):
    user_id = models.IntegerField(primary_key=True)
    task_id = models.IntegerField(primary_key=True)
    task_pinned = models.IntegerField()
    class Meta:
        db_table = u'dotp_user_task_pin'

# ================================================================================================================

class GoogleAccount(models.Model):
    google_account_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    google_account_password = models.TextField()
    google_account_email = models.TextField()
    class Meta:
        db_table = u'google_account'

# ================================================================================================================

class TimesheetConfig(models.Model):
    data = models.DateTimeField(null=True, blank=True)
    dias = models.IntegerField();
    class Meta:
        db_table = u'timesheet_config'      

    def __unicode__(self):
        return u'%s' % (self.dias )

# ================================================================================================================

class TimesheetData (models.Model):
    data = models.DateTimeField(primary_key=True)
    dia_semana = models.TextField(null=True, blank=True)
    qtd_horas = models.IntegerField()
    comentario = models.TextField(null=True, blank=True)
    class Meta:
        db_table = u'timesheet_data'

# ================================================================================================================

class TimesheetFerias(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(DotpUsers, verbose_name=u'Usuário', db_column='usuario',) 
    data_inicio =  models.DateField( db_column='datainicio', max_length=10)
    data_fim =  models.DateField( db_column='datafim', max_length=10)
    descricao = models.CharField(null=True, blank=True, max_length=20)
    class Meta:
        db_table = u'timesheet_ferias'


