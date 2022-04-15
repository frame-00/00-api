import csv
import json
import yaml

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework.authtoken.models import Token


from zerozero import forms
from zerozero.models import QueryReport
from zerozero.query import json_to_yaml, where_to_q


class TokenView(LoginRequiredMixin, View):

    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, "zerozero/token.html", self.context)

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        token, created = Token.objects.get_or_create(user=request.user)
        self.context.update({"token": token.key})
        messages.success(request, token.key)
        return HttpResponseRedirect(reverse_lazy("token-generator"))


class QueryReportMixin(object):
    def get_success_url(self):
        return reverse(
            "slug-query-report",
            kwargs={"slug": self.object.slug},
        )


class QueryReportCreate(LoginRequiredMixin, QueryReportMixin, CreateView):
    context = {}
    form_class = forms.QueryReportForm
    template_name = "zerozero/queryreport_create.html"


# TODO: these 2 need updating, and we some sort of base or redirect... /query-report/
class QueryReportList(LoginRequiredMixin, ListView):
    model = QueryReport
    template_name = "zerozero/queryreport_list.html"


class QueryReportUpdate(LoginRequiredMixin, QueryReportMixin, UpdateView):
    model = QueryReport
    form_class = forms.QueryReportForm
    template_name = "zerozero/queryreport_update.html"

    def get_object(self, queryset=None):
        """Using get_object to convert where field from json to yaml for user input"""
        obj = super().get_object(queryset)
        value = json_to_yaml(getattr(obj, "where"))
        setattr(obj, "where", value)
        return obj


# TODO Add deleteview later (by owner)
