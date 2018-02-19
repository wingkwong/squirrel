from django.views import generic
from .models import Expense


class IndexView(generic.ListView):
    template_name = "tracker/index.html"
    context_object_name = "records"

    def get_queryset(self):
        return Expense.objects.all()


class DetailView(generic.ListView):
    model = Expense
    template_name = "tracker/detail.html"
