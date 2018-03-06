from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.db.models import Sum, Count
from .tables import ExpenseTable
from .models import Expense
from .forms import ExpenseTableHelper
from .filters import ExpenseFilter
import random
from calendar import monthrange
import datetime


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
        table.order_by = '-date'
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context


class ExpenseCreate(CreateView):
    # TODO: add datepicker

    model = Expense
    fields = [
        'date',
        'description',
        'type',
        'payment',
        'amount'
    ]


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = [
        'date',
        'description',
        'type',
        'payment',
        'amount'
    ]


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('tracker:expense')


class AnalyticsView(generic.ListView):
    template_name = "analytics/index.html"
    context_object_name = "records"
    model = Expense

    def get_queryset(self):
        return Expense.objects.values('type').distinct()

    def get_expense_data(request, *args, **kwargs):
        json = serializers.serialize("json", Expense.objects.all())
        data = {"expense": json}
        return JsonResponse(data)

    def statistic(request):
        # count total record
        total_records = Expense.objects.count()

        # sum up all the expenses
        total_expenses = Expense.objects.aggregate(amount=Sum('amount'))['amount']

        # categories count
        categories = Expense.objects.values('type').annotate(the_count=Count('type')).count()

        # list out dates for the following processing.
        dates = list(Expense.objects.values('date')
                     .values_list('date', flat=True))

        # avg amount per year, per month and per day
        year_arr = []
        month_arr = []
        day_arr = []
        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
            if date.year not in month_arr:
                month_arr.append(date.month)
            if date.year not in day_arr:
                day_arr.append(date.day)

        avg_year = total_expenses / year_arr.__len__()
        avg_month = total_expenses / month_arr.__len__()
        avg_day = total_expenses / day_arr.__len__()

        now = datetime.datetime.now()

        context = {
            'context_type': 'statistic',
            'total_records': total_records,
            'total_expenses': float("{0:.2f}".format(total_expenses)),
            'categories': categories,
            'avg_year': float("{0:.2f}".format(avg_year)),
            'avg_month': float("{0:.2f}".format(avg_month)),
            'avg_day': float("{0:.2f}".format(avg_day)),
            'current_year': now.year,
            'current_month': now.month,
            'current_day': now.day

        }

        return render(request, "analytics/index.html", context)

    def annually(request, year):
        # retrieve distinct types
        expense_type = list(Expense.objects.filter(date__year=year).values('type').distinct().order_by()
                                 .values_list('type', flat=True))

        datasets = []
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        for type in expense_type:
            # expense
            arr = list(Expense.objects.filter(date__year=year).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(Expense.objects.filter(date__year=year).filter(type=type).values('date').distinct()
                            .order_by('date')
                            .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(Expense.objects.filter(date__year=year).filter(type=type)
                .values('date').distinct().order_by('date')
                .annotate(amount=Sum('amount')).values_list('amount', flat=True))

            # init array with size 12 with value 0
            monthly_expense_cnt = [0] * 12

            for i, m in enumerate(arr):
                monthly_expense_cnt[m.date.month-1] += m.amount

            total_amount = []

            for j, k in enumerate(monthly_expense_cnt):
                o = {}
                o['x'] = months[j];
                o['y'] = monthly_expense_cnt[j];
                print(o)
                total_amount.append(o)

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())

            # construct dataset
            dataset = {
                'label': type,
                'backgroundColor': color,
                'borderColor': color,
                'data': total_amount,
                'fill': 'false'
            }

            datasets.append(dataset)

        # fetch available years for menu labels
        dates = list(Expense.objects.values('date')
             .values_list('date', flat=True))
        year_arr = []
        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
        year_arr.sort()

        context = {
            'context_type': 'annually',
            'datasets': datasets,
            'labels': months,
            'title': 'Annual Report in ' + str(year),
            'report_type': 'line',
            'menu_labels': year_arr,
            'x_axis_label': 'Month'
        }

        return render(request, "analytics/index.html", context)

    def monthly(request, year, month):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        months_reverse = dict(January=1, February=2, March=3, April=4)
        datasets = []

        # retrieve distinct types
        expense_type = list(Expense.objects.filter(date__year=year).filter(date__month=month).values('type').distinct().order_by()
                            .values_list('type', flat=True))

        lastday = monthrange(year, month)[1]
        days = list(range(1,lastday+1))

        for type in expense_type:
            # expense
            arr = list(Expense.objects.filter(date__year=year).filter(date__month=month).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(Expense.objects.filter(date__year=year).filter(date__month=month).filter(type=type).values('date').distinct()
                                 .order_by('date')
                                 .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(Expense.objects.filter(date__year=year).filter(date__month=month).filter(type=type)
                                   .values('date').distinct().order_by('date')
                                   .annotate(amount=Sum('amount')).values_list('amount', flat=True))

            # init array
            daily_expense_cnt = [0] * lastday

            for i, m in enumerate(arr):
                daily_expense_cnt[m.date.day] += m.amount

            total_amount = []

            for j, k in enumerate(daily_expense_cnt[1:]):
                o = {}
                o['x'] = days[j];
                o['y'] = daily_expense_cnt[j+1];
                total_amount.append(o)

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())

            # construct dataset
            dataset = {
                'label': type,
                'backgroundColor': color,
                'borderColor': color,
                'data': total_amount,
                'fill': 'false'
            }

            datasets.append(dataset)

        # fetch available months for menu labels
        dates = list(Expense.objects.values('date')
                     .values_list('date', flat=True))
        month_arr = []
        for date in dates:
            if date.month not in month_arr:
                month_arr.append(date.month)
                month_arr.sort()


        context = {
            'context_type': 'monthly',
            'datasets': datasets,
            'monthly_expense': expense_type,
            'labels': days,
            'title': 'Monthly Report on ' + str(months[month-1]) + ' ' + str(year),
            'report_type': 'bar',
            'selected_year':year ,
            'menu_labels': month_arr,
            'x_axis_label': 'Day'
        }
        return render(request, "analytics/index.html", context)

    def daily(request, year, month, day):
        type =[]
        # retrieve distinct types
        expense_type = list(
            Expense.objects.filter(date__year=year).filter(date__month=month)
            .filter(date__day=day).values('type').distinct().order_by()
            .values_list('type', flat=True))

        datasets = []
        expense_arr = []
        color_arr = []
        for type in expense_type:
            # expense amount by type
            expense_tmp_arr = list(Expense.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)
                                   .filter(type=type)
                                   .values('date').distinct().order_by('date')
                                   .annotate(amount=Sum('amount')).values_list('amount', flat=True))
            # get the sum
            expense_arr.append(expense_tmp_arr[0])

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            color_arr.append(color)

        # construct dataset
        dataset = {
            'label': type,
            'backgroundColor': color_arr,
            'borderColor': color_arr,
            'data': expense_arr
        }

        datasets.append(dataset)

        context = {
            'context_type': 'daily',
            'datasets': datasets,
            'daily_expense': expense_type,
            'labels': expense_type,
            'title': 'Daily Report on ' + str(day) + '/' + str(month) + '/' + str(year) ,
            'report_type': 'pie'
        }
        return render(request, "analytics/index.html", context)

