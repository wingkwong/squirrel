from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Sum, Count
from django.db import models
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
        return Expense.objects.filter(created_by=self.request.user)

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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.created_at = datetime.datetime.now()
        obj.save()
        return HttpResponseRedirect(reverse_lazy('tracker:expense'))


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = [
        'date',
        'description',
        'type',
        'payment',
        'amount'
    ]

# obsolete
class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('tracker:expense')


class AnalyticsView(generic.ListView):
    template_name = "analytics/index.html"
    context_object_name = "records"
    model = Expense

    def statistic(request):
        # init
        avg_year = 0
        avg_month = 0
        avg_day = 0

        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        # count total record
        total_records = exp.count()

        # sum up all the expenses
        total_expenses = exp.aggregate(amount=Sum('amount'))['amount']
        if total_expenses is None:
            total_expenses = 0

        # categories count
        categories = exp.values('type').annotate(the_count=Count('type')).count()

        # list out dates for the following processing.
        dates = list(exp.values('date')
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

        if total_expenses > 0 :
            avg_year = float("{0:.2f}".format(total_expenses / year_arr.__len__()))
            avg_month = float("{0:.2f}".format(total_expenses / month_arr.__len__()))
            avg_day = float("{0:.2f}".format(total_expenses / day_arr.__len__()))
            total_expenses = float("{0:.2f}".format(total_expenses))

        now = datetime.datetime.now()

        context = {
            'context_type': 'statistic',
            'total_records': total_records,
            'total_expenses': total_expenses,
            'categories': categories,
            'avg_year': avg_year,
            'avg_month': avg_month,
            'avg_day': avg_day,
            'current_year': now.year,
            'current_month': now.month,
            'current_day': now.day

        }

        return render(request, "analytics/index.html", context)

    def annually(request, year):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        # retrieve distinct types
        expense_type = list(exp.filter(date__year=year).values('type').distinct().order_by()
                                 .values_list('type', flat=True))

        datasets = []
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        for type in expense_type:
            # expense
            arr = list(exp.filter(date__year=year).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(exp.filter(date__year=year).filter(type=type).values('date').distinct()
                            .order_by('date')
                            .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(type=type)
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
        dates = list(exp.values('date')
             .values_list('date', flat=True))
        year_arr = []
        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
        year_arr.sort()

        # construct submenu
        expense_per_month = []
        month_not_none = []
        for i, month in enumerate(months):
            amount = exp.filter(date__year=year).filter(date__month=(i+1)).values('date').distinct().order_by('date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_month.append(float("{0:.2f}".format(amount)))
                month_not_none.append((i+1))

        if expense_per_month:
            submenu = zip(month_not_none, expense_per_month)
        else:
            submenu = False

        context = {
            'context_type': 'annually',
            'datasets': datasets,
            'labels': months,
            'title': 'Annual Report in ' + str(year),
            'report_type': 'line',
            'menu_labels': year_arr,
            'x_axis_label': 'Month',
            'submenu': submenu
        }

        return render(request, "analytics/index.html", context)

    def monthly(request, year, month):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        months_reverse = dict(January=1, February=2, March=3, April=4)
        datasets = []

        # retrieve distinct types
        expense_type = list(exp.filter(date__year=year).filter(date__month=month).values('type').distinct().order_by()
                            .values_list('type', flat=True))

        lastday = monthrange(year, month)[1]
        days = list(range(1,lastday+1))

        for type in expense_type:
            # expense
            arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type).values('date').distinct()
                                 .order_by('date')
                                 .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type)
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
        dates = list(exp.values('date')
                     .values_list('date', flat=True))
        month_arr = []
        for date in dates:
            if date.month not in month_arr:
                month_arr.append(date.month)
                month_arr.sort()

        # construct submenu
        expense_per_day = []
        day_not_none  = []
        for i, d in enumerate(days):
            amount = exp.filter(date__year=year).filter(date__month=month).filter(date__day=(i+1)).values('date').distinct().order_by(
                'date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_day.append(float("{0:.2f}".format(amount)))
                day_not_none.append((i+1))

        if expense_per_day:
            submenu = zip(day_not_none, expense_per_day)
        else:
            submenu = False
        
        context = {
            'context_type': 'monthly',
            'datasets': datasets,
            'monthly_expense': expense_type,
            'labels': days,
            'title': 'Monthly Report on ' + str(months[month-1]) + ' ' + str(year),
            'report_type': 'bar',
            'selected_year':year ,
            'menu_labels': month_arr,
            'x_axis_label': 'Day',
            'submenu': submenu
        }
        return render(request, "analytics/index.html", context)

    def daily(request, year, month, day):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        type =[]
        # retrieve distinct types
        expense_type = list(
            exp.filter(date__year=year).filter(date__month=month)
            .filter(date__day=day).values('type').distinct().order_by()
            .values_list('type', flat=True))

        datasets = []
        expense_arr = []
        color_arr = []
        for type in expense_type:
            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(date__day=day)
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
        if color_arr and expense_arr:
            dataset = {
                'label': type,
                'backgroundColor': color_arr,
                'borderColor': color_arr,
                'data': expense_arr
            }
            datasets.append(dataset)

        # construct submenu
        expense_per_type = []
        for i, type in enumerate(expense_type):
            amount = exp.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(type=type).values('date').distinct().order_by('date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_type.append(float("{0:.2f}".format(amount)))

        if expense_per_type:
            submenu = zip(expense_type, expense_per_type)
        else:
            submenu = False

        context = {
            'context_type': 'daily',
            'datasets': datasets,
            'daily_expense': expense_type,
            'labels': expense_type,
            'title': 'Daily Report on ' + str(day) + '/' + str(month) + '/' + str(year) ,
            'x_axis_label': 'Type',
            'report_type': 'pie',
            'submenu': submenu
        }
        return render(request, "analytics/index.html", context)

