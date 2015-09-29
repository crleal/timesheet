from django.conf.urls.defaults import *
from smart_selects import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import *
from projeto.views import *

#import reporting

admin.autodiscover()
#reporting.autodiscover()   

urlpatterns = patterns('',
    # Example:
    # (r'^timesheet/', include('timesheet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^chaining/', include('smart_selects.urls')),
    (r'^cadastros/', include(admin.site.urls)),
    (r'^$','projeto.views.index_usuario'),
    (r'^assumir/(?P<id>\d+)','projeto.views.assumiros'),
    (r'^encerradoos/(?P<id>\d+)','projeto.views.encerradoos'),
    (r'^ordemservico/', 'projeto.views.ordemservicointranet'),
    (r'^usuariohoras/', 'projeto.views.usuariohoras'),
    (r'^resumohoras/', 'projeto.views.resumohoras'),
    (r'^resumohorasintranet/', 'projeto.views.resumohorasintranet'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
#    (r'^reporting/', include('reporting.urls')),  
    (r'^atualizarperc/','projeto.views.atualizaperc'),
    (r'^usuariodia/(?P<usuarioid>\d+)/(?P<ano>\d+)/(?P<mes>\d+)/(?P<dia>\d+)','projeto.views.usuariodia'),

)
