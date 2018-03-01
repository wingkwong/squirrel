import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')
    payment = django_filters.CharFilter(lookup_expr='icontains')
    amount = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Expense
        fields = (
            'description',
            'type',
            'payment',
            'amount',
            'date'
        )