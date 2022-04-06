from django.urls import include, path

from . import views

urlpatterns = [
    path("token/", views.TokenView.as_view(), name="token-generator"),
    path(
        "query-report/create",
        views.QueryReportCreate.as_view(),
        name="create-query-report",
    ),
    path(
        "query-report/<slug:slug>/",
        views.QueryReportUpdate.as_view(),
        name="slug-query-report",
    ),
    path(
        "query-report/list",
        views.QueryReportList.as_view(),
        name="list-query-report",
    ),
    path(
        "query-report/update",
        views.QueryReportUpdate.as_view(),
        name="update-query-report",
    ),
]
