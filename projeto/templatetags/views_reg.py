from django import template
from projeto.models import Timesheet, DotpUsers, Os
from django.http import QueryDict
from django.db.models import Count

register = template.Library()

class TimesheetNode(template.Node):
    def __init__(self, limit, varname, user):
        self.limit, self.varname, self.user = limit, varname, user

    def __repr__(self):
        return "<GetTimesheet Node>"

    def render(self, context):
        if self.user is None:
            context[self.varname] = Timesheet.objects.all().order_by('-data','-hora_inicio')[:self.limit]
        else:
            user_id = self.user
            if not user_id.isdigit():
                user_id = context[self.user].id
            context[self.varname] = Timesheet.objects.filter(usuario__exact=user_id).order_by('-data','-hora_inicio')[:self.limit]
        return ''

class DoGetTimesheet:
    """
    Populates a template variable with the admin log for the given criteria.

    Usage::

        {% get_admin_log [limit] as [varname] for_user [context_var_containing_user_obj] %}

    Examples::

        {% get_admin_log 10 as admin_log for_user 23 %}
        {% get_admin_log 10 as admin_log for_user user %}
        {% get_admin_log 10 as admin_log %}

    Note that ``context_var_containing_user_obj`` can be a hard-coded integer
    (user ID) or the name of a template context variable containing the user
    object whose ID you want.
    """
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 4:
            raise template.TemplateSyntaxError("'%s' statements require two arguments" % self.tag_name)
        if not tokens[1].isdigit():
            raise template.TemplateSyntaxError("First argument in '%s' must be an integer" % self.tag_name)
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError("Second argument in '%s' must be 'as'" % self.tag_name)
        if len(tokens) > 4:
            if tokens[4] != 'for_user':
                raise template.TemplateSyntaxError("Fourth argument in '%s' must be 'for_user'" % self.tag_name)
        return TimesheetNode(limit=tokens[1], varname=tokens[3], user=(len(tokens) > 5 and tokens[5] or None))



@register.filter
def pegatotalmesdep(anomes, args):
    total1 = Os.objects.filter(dept_id=args, data__year=anomes['ano'], data__month=anomes['anomes']).count()
    if total1 == 0:
       total1 = ""  
    return ('%s') % (total1)

@register.filter
def pegatotalhorasmesdep(anomes, args):

    #total1 = Timesheet.objects.filter(dept_id=args, data__year=anomes['ano'], data__month=anomes['anomes']).sum()
    total1 = sum([i['horastrab'] for i in Timesheet.objects.filter(ticket__isnull=False, ticket__dept_id=args, 
                      data__year=anomes['ano'], data__month=anomes['anomes']).values('horastrab')])
    if total1 == 0:
       total1 = ""  
    return ('%s') % (total1 )




register.tag('get_timesheet', DoGetTimesheet('get_timesheet'))

