# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext
from models import *
from django.template import Context
from django import template
from forms import * 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

@login_required
def index_usuario(request):
    return index_usuario1(request, "")

def index_usuario1(request, msg):
    tickets = Os.objects.filter(assignment__isnull=True).exclude(ctype = 'Closed')     
    ticketsaberto = Os.objects.filter(assignment = request.user.id).exclude(ctype = 'Closed')    
    #atividades = Atividades.objects.filter(task_owner=request.user.id, task_percent_complete__lt=100)
    atividades = DotpUserTasks.objects.filter(user_id=request.user.id, 
              task_id__task_percent_complete__lt=100,
              task_id__task_project__project_status__in=(0,2,3,4,5,6) ).order_by('task_id__task_end_date')
    if msg:
       msg = msg
    return render_to_response('index_usuario.html',
                   locals(), context_instance=RequestContext(request))
                   
# ================================================================================================================

def atualizaperc(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    for i in range(1, 6): 
       cursor.execute("update dotp_tasks tas  , \
                      (SELECT t.task_id, t.task_percent_complete , tt.percfinal \
                       FROM dotp_tasks t, (SELECT task_parent , sum( task_percent_complete ), \
                                           count( task_id ) , truncate( sum( task_percent_complete ) / count( task_id ) , 0 ) percfinal \
                                           FROM dotp_tasks  \
                                           WHERE task_id <> task_parent \
                                           GROUP BY task_parent )tt \
                       WHERE t.task_id = tt.task_parent  and  t.task_percent_complete <> tt.percfinal) tfff \
                    set  tas.task_percent_complete = tfff.percfinal  where tas.task_id = tfff.task_id ")
    transaction.commit_unless_managed()
    return index_usuario(request)
            
# ================================================================================================================

def assumiros(request, id):
    usur = DotpUsers.objects.get(user_id=request.user.id)
    #ticket = Os.objects.filter(ticket=id, assignment__isnull=True).update(assignment = usur)

    ticketos = Os.objects.get(ticket=id)
    mensagemerro = ""
    if ticketos and (ticketos.assignment==None):
       ticketos.assignment = request.user       
       ticketos.save() 
       try:       
         if  ticketos.mandar_email == 'S':
           origem_email = 'suporte_ti@foreverliving.com.br' 
           email = ticketos.email
           titulo = ticketos.subject
           texto = u"""
                 O atendimento da solicitação de número: %s já esta em curso.
                  
                 Solicitante: %s
                 E-mail: %s
                 Departamento: %s
                 Tipo de Solicitação: %s
                 Solicitação: %s  

                 Mensagem:
                 %s
                 """ % (id, ticketos.author, ticketos.email, ticketos.dept_id, ticketos.ticket_tipo_os, ticketos.subject, ticketos.body )
           send_mail(subject=titulo, message=texto, from_email=origem_email, recipient_list=[email],) 
       except:
           mensagemerro = "OS assumida mas não foi possível notificar por e-mail!"
    return index_usuario1(request, mensagemerro)
    
# ================================================================================================================

def encerradoos(request, id):
    ticket = Os.objects.get(ticket=id)
    mensagemerro = ""
    if ticket.ctype != 'Closed':
       ticket.ctype = 'Closed'
       ticket.save()
       mensagemerro = ""
       try:
          if ticket.mandar_email == 'S':
             origem_email = 'suporte_ti@foreverliving.com.br' 
             email = ticket.email
             titulo = ticket.subject
             texto = u"""
                 O atendimento da solicitação de número: %s foi concluido.
                  
                 Solicitante: %s
                 E-mail: %s
                 Departamento: %s
                 Tipo de Solicitação: %s
                 Solicitação: %s  

                 Mensagem:
                 %s
                 """ % (id, ticket.author, ticket.email, ticket.dept_id, ticket.ticket_tipo_os, ticket.subject, ticket.body )
             send_mail(subject=titulo, message=texto, from_email=origem_email, recipient_list=[email],) 
       except:
             mensagemerro = "OS encerrada mas não foi possível notificar por e-mail!"
    return index_usuario1(request, mensagemerro)



#   import urllib2
#   u = urllib2.urlopen('http://192.168.0.174/intranet/_layouts/userdisp.aspx?&ID=50')
#   u.read(
# ================================================================================================================

def ordemservicointranet(request):

    if request.POST:
       
       form = FormOrdemServicoInternet(request.POST, request.FILES,)
       if form.is_valid():
          osservico = form.save(commit=False)  
          osservico.end_ip = request.META['REMOTE_ADDR']
          osservico.mandar_email = 'S'
          mensagemerro = ''
          try:
             form.enviar()            
          except: 
             mensagemerro = 'Não foi possivel enviar o e-mail de confirmação!' 
          #osarquivo_formset = OsArquivoFormSet(request.POST, request.FILES, instance=osservico)
          #if osarquivo_formset.is_valid():
          #   osservico.save()
          #   osarquivo_formset.save() 
          osservico.save()       
          #osarquivo_formset.save() 
          mostrar = u'Solicitação %s enviada!' % (osservico.ticket)
          form = FormOrdemServicoInternet() 
          #formset = OsArquivoFormSet(instance=Os())
          return render_to_response('ordemservico.html',
                   locals(), context_instance=RequestContext(request))
       else:
          HttpResponse(form.errors)
    else:
          form = FormOrdemServicoInternet()
          #formset = OsArquivoFormSet(instance=Os())

    return render_to_response('ordemservico.html',
                   locals(), context_instance=RequestContext(request))

# ================================================================================================================

def usuariohoras(request):

#      tt = self.timesheet.objects.raw('SELECT dt.username usuario, dt.data, dt.dia_semana, round( sum( `horastrab` ) ) horas '+
#                                  'FROM timesheet time '+
#                                  '         RIGHT JOIN (SELECT id, username, dt. * FROM auth_user, timesheet_data dt)dt ON ( time.data = dt.data AND time.usuario = dt.id ) , '+ 
#                                  '                    (SELECT usuario FROM timesheet GROUP BY usuario ) usu '+ 
#                                  'WHERE (usu.usuario = dt.id) '+
#                                  '  and (usu.usuario = '+ self.user_id + ')' +
#                                  'GROUP BY dt.username, dt.data, dt.dia_semana '+
#                                  'ORDER BY  data desc')


    if request.user.is_superuser:   
        ppp = Timesheet.objects.annotate(contador=Count('usuario') ).values_list('usuario').query 
    else:
        ppp = Timesheet.objects.filter(usuario=request.user.id).annotate(contador=Count('usuario') ).values_list('usuario').query 

    usu = User.objects.all().filter(id__in=ppp, is_active__exact = 1).values_list('id').query 

    dusuarios = DotpUsers.objects.all().filter(user_id__in=usu)




    form = Periodo(request.POST)
    if request.method == 'POST':
      if form.is_valid(): 
            telefone = form.cleaned_data['telefone']
        
            if request.user.is_superuser:   
               ppp = Timesheet.objects.annotate(contador=Count('usuario') ).values_list('usuario').query 
            else:
               ppp = Timesheet.objects.filter(usuario=request.user.id).annotate(contador=Count('usuario') ).values_list('usuario').query 

            usu = User.objects.all().filter(id__in=ppp, is_active__exact = 1).values_list('id').query 
            dusuarios = DotpUsers.objects.all().filter(user_id__in=usu)

            return render_to_response('usuariohoras.html',
                   locals(), context_instance=RequestContext(request))

    return render_to_response('usuariohoras.html',
                   locals(), context_instance=RequestContext(request))

# ================================================================================================================    

def resumohoras(request):

    timesheet = Timesheet.objects.aggregate(total=Sum('horastrab') ) 

    somaatividade = sum([i['horastrab'] for i in Timesheet.objects.filter(task_id__isnull=False).values('horastrab')])
    somaos = sum([i['horastrab'] for i in Timesheet.objects.filter(ticket__isnull=False).values('horastrab')])

    os_anomes = Os.objects.extra(
                               select={ 'anomes': 'MONTH(data)', 'ano': 'YEAR(data)' }
                             ).values( 'anomes', 'ano'
                                      ).annotate(total=Count('data')).order_by('ano','anomes', 'total')
     
    os_dep_dept = Os.objects.values('dept_id__dept_name','dept_id').annotate(total=Count('dept_id')).order_by('dept_id__dept_name')
    

    '''
    os_dep = Os.objects.extra(
                               select={ 'anomes': 'MONTH(data)', 'ano': 'YEAR(data)' }
                             ).values( 'dept_id__dept_name','anomes', 'ano', 'dept_id'
                                      ).annotate(total=Count('dept_id__dept_name')
                                      ).order_by('ano','anomes','dept_id__dept_name', 'dept_id','total')
    '''


    os_anomes_horas = Timesheet.objects.filter(ticket__isnull = False
                                            ).extra(
                                              select={ 'anomes': 'MONTH(data)', 'ano': 'YEAR(data)' }
                                             ).values( 'anomes', 'ano'
                                             ).annotate(total=Sum('horastrab')).order_by('ano','anomes', 'total')

    os_dep_horas = Timesheet.objects.filter(ticket__isnull = False
                                            ).values('ticket__dept_id__dept_name', 'ticket__dept_id__dept_id'
                                      ).annotate(total=Sum('horastrab')).order_by('ticket__dept_id__dept_name')

    return render_to_response('resumohoras.html',
                   locals(), context_instance=RequestContext(request))


def resumohorasintranet(request):
    os_anomes = Os.objects.extra(
                               select={ 'anomes': 'MONTH(data)', 'ano': 'YEAR(data)' }
                             ).values( 'anomes', 'ano'
                                      ).annotate(total=Count('data')).order_by('ano','anomes', 'total')
     
    os_dep_dept = Os.objects.values('dept_id__dept_name','dept_id').annotate(total=Count('dept_id')).order_by('dept_id__dept_name')
    
    return render_to_response('resumohoras_intranet.html',
                   locals(), context_instance=RequestContext(request))



# ================================================================================================================    

def usuariodia(request, usuarioid, ano, mes, dia):

    timesheet = Timesheet.objects.filter(usuario=usuarioid, data__year=ano, data__month=mes, data__day=dia ) #.order_by('hora_inicio') 

    return render_to_response('usuariodia.html',
                   locals(), context_instance=RequestContext(request))


