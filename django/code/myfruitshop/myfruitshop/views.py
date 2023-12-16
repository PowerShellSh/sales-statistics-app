from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from sales.models import Fruit

class TopPageView(LoginRequiredMixin, ListView):
    template_name = 'top.html'
    context_object_name = 'fruits'
    model = Fruit
