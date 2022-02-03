from django.urls import include, path

from zerozero import views

urlpatterns = [
    path("token/", views.TokenView.as_view(), name="token-generator"),
    path(
        "query-report/create",
        views.QueryReportCreate.as_view(),
        name="create-query-report",
    ),
]
