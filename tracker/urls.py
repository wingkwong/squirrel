from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'tracker'

urlpatterns = [
	# /
    path('', views.landingView.landing, name ="landing"),

    # /dashboard
    path('dashboard', login_required(views.Dashboard.index), name="dashboard"),

    # /tracker
    path('tracker', login_required(views.IndexView.as_view()), name ="expense"),

    # /add
    path('tracker/add', login_required(views.ExpenseCreate.as_view()), name="create_expense"),

    # /update/{id}
    path('tracker/update/<int:pk>', login_required(views.ExpenseUpdate.as_view()), name="update_expense"),

    # /delete/{id}
    path('tracker/delete/<int:pk>', login_required(views.ExpenseDelete.as_view()), name="delete_expense"),

    # /analytics
    # FIXME: redirect to dashboard
    path('analytics', login_required(views.Dashboard.index), name="analytics"),

    # /analytics/2018
    path('analytics/<int:year>', login_required(views.AnalyticsView.annually), name="annually"),

    # /analytics/2018/02
    path('analytics/<int:year>/<int:month>', login_required(views.AnalyticsView.monthly), name="monthly"),

    # /analytics/2018/02/20
    path('analytics/<int:year>/<int:month>/<int:day>', login_required(views.AnalyticsView.daily), name="daily"),
]
