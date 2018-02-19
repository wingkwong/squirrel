from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Expense


class IndexView(generic.ListView):
    template_name = "tracker/index.html"
    context_object_name = "records"

    def get_queryset(self):
        return Expense.objects.all()


class DetailView(generic.DetailView):
    model = Expense
    template_name = "tracker/detail.html"


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
    success_url = reverse_lazy('tracker:index')
