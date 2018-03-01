import django_tables2 as tables
from django_tables2.utils import A
from .models import Expense


class ExpenseTable(tables.Table):
    class Meta:
        model = Expense
        fields = (
            'date',
            'description',
            'type',
            'payment',
            'amount',
            )
        attrs = {"class": "table table-striped table-bordered dt-responsive nowrap"}
        empty_text = "No records found"
        template_name = 'django_tables2/bootstrap.html'

