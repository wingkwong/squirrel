from django.shortcuts import render, get_object_or_404
from .models import Expense


def index(request):
    records = Expense.objects.all()
    return render(request, 'tracker/index.html', {
        'records': records
    })


def detail(request, expense_id):
    records = get_object_or_404(Expense, pk=expense_id)
    return render(request, 'tracker/detail.html', {'records': records})
