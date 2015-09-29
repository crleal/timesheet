import reporting
from django.db.models import Sum, Avg, Count
from models import Timesheet

class TimesheetReport(reporting.Report):
    model = Timesheet
    verbose_name = 'Timesheet Report'
    annotate = (                    # Annotation fields (tuples of field, func, title)
        ('id', Count, 'Total'),     # example of custom title for column 
        ('horastrab', Sum),            # no title - column will be "Salary Sum"

    )
    aggregate = (                   # columns that will be aggregated (syntax is the same as for annotate)
        ('id', Count, 'Total'),
        ('horastrab', Sum, 'horastrab'),
    )
    group_by = [                   # list of fields and lookups for group-by options
        'usuario',
        'data',
    ]
    list_filter = [                # This are report filter options (similar to django-admin)
       'occupation',
       'country',
    ]
    
    detail_list_display = [        # if detail_list_display is defined user will be able to see how rows was grouped  
        'usuario', 
        'data',
    ]

    date_hierarchy = 'data' # the same as django-admin


reporting.register('timesheet', TimesheetReport) # Do not forget to 'register' your class in reports
