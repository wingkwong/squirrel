import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .models import Expense


class ActionButtons(tables.Column):
    empty_values = list()
    def render(self, value, record):
        html = "<a href=/tracker/update/%s class='btn btn-info'><i class='material-icons'>&#xE254;</i></a>" % escape(record.id)
        return mark_safe(html)


class ExpenseTable(tables.Table):
    actions = ActionButtons()
    class Meta:
        model = Expense
        fields = (
            'date',
            'description',
            'type',
            'payment',
            'amount'
            )
        attrs = {"class": "table table-striped dt-responsive nowrap"}
        empty_text = "No records found"
        template_name = 'django_tables2/bootstrap-responsive.html'

