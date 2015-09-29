# -*- coding: utf-8 -*-
from django.contrib import admin
from models import DotpCompanies, DotpProjects, DotpDepartments, DotpProjectDepartments
from models import DotpProjectContacts, DotpContacts, Atividades, DotpTaskContacts, DotpTaskDepartments
from models import Os, DotpUsers, Timesheet, DotpUserTasks, TipoOs, DotpUserOS, TimesheetConfig, TimesheetFerias, TimesheetConsulta
from forms import *
from django.forms.models import BaseInlineFormSet

from django.db.models import Count


from utils.utils import *


#inlines
class DotpProjectDepartmentsInline(admin.TabularInline):
    model = DotpProjectDepartments
    extra = 1

class DotpProjectContactsInline(admin.TabularInline):
    model = DotpProjectContacts
    extra = 1

class DotpTaskContactsInline(admin.TabularInline):
    model = DotpTaskContacts
    extra = 1

class DotpUserTasksInline(admin.TabularInline):
    model = DotpUserTasks
    extra = 1
    
class DotpTaskDepartmentsInline(admin.TabularInline):
    model = DotpTaskDepartments
    extra = 1
###

class DotpProjectsAdmin(admin.ModelAdmin):
    inlines = (DotpProjectContactsInline,)
    list_display = ('project_name','project_owner','project_departments')
    list_filter = ('project_owner',)
    search_fields = ('project_name','project_departments',)
    list_per_page = 40
    ordering = ('project_name',)
    actions = None
    #form = DotpProjectsForm 
    #change_form_template = 'projeto/change_form.html'

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)

# ================================================================================================================

class DotpDepartmentsAdmin(admin.ModelAdmin):
    list_display = ('dept_name','indica_filial')
    #list_filter = ('',)
    search_fields = ('dept_name',)
    list_per_page = 40
    ordering = ('dept_name',)
    actions = None
    #form = DotpProjectsForm 
    #change_form_template = 'projeto/change_form.html'

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)

# ================================================================================================================

class DotpContactsAdmin(admin.ModelAdmin):
    list_display = ('contact_first_name','contact_last_name','contact_email',)
    #list_filter = ('',)
    search_fields = ('contact_first_name',)
    list_per_page = 40
    ordering = ('contact_first_name',)
    actions = None
    #form = DotpProjectsForm 
    #change_form_template = 'projeto/change_form.html'

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)

# ================================================================================================================

class AtividadesAdmin(admin.ModelAdmin):
    inlines = (DotpUserTasksInline, )
    list_display = ('task_name', 'task_project' ,'task_owner',)
    #list_display_links = ('task_name',)
    #list_filter = ('',)
    search_fields = ('task_project', 'task_name','task_owner',)
    list_per_page = 40
    ordering = ('task_project','task_name',)
    actions = None
    #form = DotpProjectsForm 
    #change_form_template = 'projeto/change_form.html'

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)

# ================================================================================================================

class TimeOsInline(admin.TabularInline):
    model = TimesheetConsulta
    fields = ('usuario', 'data', 'hora_inicio', 'hora_final', 'cometarios')
    readonly_fields = ('usuario', 'data', 'hora_inicio', 'hora_final', 'cometarios')
    extra=0
    can_delete = False
    max_num=0
     
    def has_change_permission(self, request, obj=None):   
        return False
        #return super(MyAdmin, self).has_delete_permission(request, obj))


class DotpUserOSInLine(admin.TabularInline):
    model = DotpUserOS
    #fields = ('usuario', 'data', 'hora_inicio', 'hora_final', 'cometarios')
    #extra=0
    #can_delete = False

# ================================================================================================================

class OsAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'tipo','subject','dept_id','dept_id_filial','author', 'ramal', 'situacao', 'prioridade', 'usuario_', 'data_')
    #list_display_links = ('task_name',)
    date_hierarchy = 'data' 
    list_filter = ('ctype',  'ticket_tipo_os__dsc_os', 'priority', 'dept_id', 'assignment')
    search_fields = ('ticket','subject', 'author','assignment__username','ticket_tipo_os__dsc_os', 'body',)
    list_per_page = 40
    #ordering = ('task_project','task_name',)
    actions = None
    form = FormOS
    #change_form_template = 'projeto/change_form.html'
    inlines = [ TimeOsInline ] 
    #inlines = [ DotpUserOSInLine ] #TimeOsInline, ]
    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)   

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dept_id":
               kwargs["queryset"] = DotpDepartments.objects.filter(indica_filial = 0).order_by('dept_name')
        if db_field.name == "dept_id_filial":
               kwargs["queryset"] = DotpDepartments.objects.filter(indica_filial = 1).order_by('dept_name')
        if db_field.name == "assignment":
               kwargs['initial'] = request.user.id


        return super(OsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# ================================================================================================================

class TimesheetAdmin(admin.ModelAdmin):
    list_display = ['usuario_', 'os', 'atividade', 'data_', 'hora_inicio', 'hora_final', 'tempo_trab']    
    #list_filter = ('data',)
    search_fields = ('usuario__user_username', 'ticket__ticket', )
    readonly_fields = ('horastrab',)
    list_per_page = 40
    ordering = ('-data','-hora_inicio',)
    actions = None    
    date_hierarchy = 'data'
    form = TimesheetModelForm 
    change_form_template = 'timesheet/change_form.html'
  
    def queryset(self, request):
        qs = super(TimesheetAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user).order_by('-data','-hora_inicio')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:           
           if db_field.name == "ticket":
               kwargs["queryset"] = Os.objects.filter(assignment=request.user).exclude(ctype = 'Closed').order_by('subject')
           if db_field.name == "task_id":
               ppp = Atividades.objects.annotate(contador=Count('task_parent') ).filter(contador__gt=1).values_list('task_parent').query
	       usutask = DotpUserTasks.objects.filter(user_id=request.user.id, task_id__task_percent_complete__lt=100).values('task_id').query
               kwargs["queryset"] = Atividades.objects.filter(task_id__in=usutask, 
                                task_project__project_status__in=(0,2,3,4,5,6) ).exclude(task_id__in=ppp).order_by('task_project','task_parent') 
           if db_field.name == "usuario":
               kwargs["queryset"] = DotpUsers.objects.filter(user_contact=request.user.id)
               kwargs['initial'] = request.user.id

        return super(TimesheetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)   


# ================================================================================================================

class TipoOsAdmin(admin.ModelAdmin):
    list_display = ['dsc_os', 'parent', 'intranet']    
    actions = None
    
    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)
        
        
# ================================================================================================================        

class TimesheetConfigAdmin(admin.ModelAdmin):
#    list_display = ('dsc_os', 'dsc_os_volpe')
    
    actions = None
    
    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)
        
        
# ================================================================================================================        

class TimesheetFeriasAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_inicio', 'data_fim']    
    #list_filter = ('usuario',)
    search_fields = ('usuario__user_username',  )
    list_per_page = 40
    ordering = ('data_inicio',)
    actions = None
    #date_hierarchy = 'data'
    #form = TimesheetModelForm 
    #change_form_template = 'timesheet/change_form.html'
  

    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        return troca_message(self, request, form, formsets)   

# ================================================================================================================


admin.site.register(DotpProjects, DotpProjectsAdmin)
admin.site.register(DotpDepartments, DotpDepartmentsAdmin)
admin.site.register(DotpContacts, DotpContactsAdmin)
admin.site.register(Atividades, AtividadesAdmin)
admin.site.register(Os, OsAdmin)
admin.site.register(TipoOs, TipoOsAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(TimesheetConfig, TimesheetConfigAdmin)
admin.site.register(TimesheetFerias, TimesheetFeriasAdmin)
