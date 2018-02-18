from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Hello World</h1>")


def detail(request, expense_id):
    return HttpResponse("<h2>Detail page for id: " + str(expense_id) + "</h2>")
