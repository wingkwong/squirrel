from django.urls import path
from . import views

urlpatterns = [
    # /tracker
    path('', views.index, name ="index"),

    # /tracker/{id}
    path('<int:expense_id>', views.detail, name="detail")
]