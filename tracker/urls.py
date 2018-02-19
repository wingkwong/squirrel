from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # /tracker
    path('', views.IndexView.as_view(), name ="index"),

    # /tracker/{id}
    path('<int:expense_id>', views.DetailView.as_view(), name="detail")
]