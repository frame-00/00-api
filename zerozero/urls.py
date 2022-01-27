from django.urls import include, path

from . import views

urlpatterns = [
    path("token/", views.TokenView.as_view(), name="token-generator"),
]
