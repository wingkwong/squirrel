from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # /tracker
    path('', views.index, name ="index"),

    # /tracker/{id}
    path('<int:expense_id>', views.detail, name="detail")
]