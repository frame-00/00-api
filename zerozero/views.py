from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from rest_framework.authtoken.models import Token

from zerozero import forms
from zerozero.models import QueryReport


class TokenView(LoginRequiredMixin, View):

    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, "token.html", self.context)

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        token, created = Token.objects.get_or_create(user=request.user)
        self.context.update({"token": token.key})
        messages.success(request, token.key)
        return HttpResponseRedirect(reverse_lazy("token-generator"))


class QueryReportCreate(LoginRequiredMixin, CreateView):
    model = QueryReport
    form = forms.QueryReportForm
    fields = "__all__"
