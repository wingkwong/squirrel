from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # /
    path('tracker', views.IndexView.as_view(), name ="expense"),

    # /add
    path('tracker/add', views.ExpenseCreate.as_view(), name="create_expense"),

    # /update/{id}
    path('tracker/update/<int:pk>', views.ExpenseUpdate.as_view(), name="update_expense"),

    # /delete/{id}
    path('tracker/delete/<int:pk>', views.ExpenseDelete.as_view(), name="delete_expense"),

    # /analytics
    path('analytics', views.AnalyticsView.statistic, name="analytics"),

    # /analytics/2018
    path('analytics/<int:year>', views.AnalyticsView.annually, name="annually"),

    # /analytics/2018/02
    path('analytics/<int:year>/<int:month>', views.AnalyticsView.monthly, name="monthly"),

    # /analytics/2018/02/20
    path('analytics/<int:year>/<int:month>/<int:day>', views.AnalyticsView.daily, name="daily"),

    # /analytics
    path('api/expense/', views.AnalyticsView.get_expense_data, name="api-expense")
]
