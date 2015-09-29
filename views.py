# coding:utf-8
from django.shortcuts import render_to_response, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.core.mail import send_mail

from django.http import HttpRequest
import uuid

def index(request):
    return render_to_response(
                              'index.html',
                              locals(),
                              context_instance=RequestContext(request),)


def RegistrarMaquina(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))

    for k in  request.COOKIES:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, ' '))
    '''
    html = []
    cookie = HttpResponse() 
    from datetime import datetime, timedelta 
    cookie.set_cookie("carrinho", value='teste',max_age=None, expires=datetime.now()+timedelta(days=30), 
             path="/", domain=None, secure=False, httponly=False)
    '''


    return HttpResponse('<table>%s</table>' % '\n'.join(html))
