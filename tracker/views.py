from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.core import serializers
from .tables import ExpenseTable
from .models import Expense
from .forms import ExpenseTableHelper
from .filters import ExpenseFilter
from django.shortcuts import render

class IndexView(generic.ListView):
    template_name = "tracker/index.html"
    context_object_name = "records"
    model = Expense
    table_class = ExpenseTable
    filter_class = ExpenseFilter
    formhelper_class = ExpenseTableHelper

    def get_queryset(self):
        return Expense.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        filter = ExpenseFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = ExpenseTableHelper()
        table = ExpenseTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class ExpenseCreate(CreateView):
    model = Expense
    fields = [
        'currency',
        'description',
        'type',
        'payment',
        'amount',
        'date'
    ]


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = [
        'currency',
        'description',
        'type',
        'payment',
        'amount',
        'date'
    ]


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('tracker:expense')


class AnalysisView(generic.ListView):
    template_name = "analysis/index.html"
    context_object_name = "records"
    model = Expense

    def get_queryset(self):
        return Expense.objects.values('type').distinct()

    def get_expense_data(request, *args, **kwargs):
        json = serializers.serialize("json", Expense.objects.all())
        data = {"expense": json}
        return JsonResponse(data)

    def annually(request, year):
        context = {
            'annually_expense': Expense.objects.filter(date__year=year)
        }
        return render(request, "analysis/index.html", context)

    def monthly(request, year, month):
        context = {
            'monthly_expense': Expense.objects.filter(date__year=year).filter(date__month=month)
        }
        return render(request, "analysis/index.html", context)

    def daily(request, year, month, day):
        context = {
            'daily_expense': Expense.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)
        }
        return render(request, "analysis/index.html", context)

