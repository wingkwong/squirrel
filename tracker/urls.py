from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # /tracker
    path('', views.IndexView.as_view(), name ="index"),

    # /tracker/{id}
    path('<int:pk>', views.DetailView.as_view(), name="detail"),

    # /tracker/add
    path('add', views.ExpenseCreate.as_view(), name="create_expense"),

    # /tracker/update/{id}
    path('update/<int:pk>', views.ExpenseUpdate.as_view(), name="update_expense"),

    # /tracker/delete/{id}
    path('delete/<int:pk>', views.ExpenseDelete.as_view(), name="delete_expense"),
]