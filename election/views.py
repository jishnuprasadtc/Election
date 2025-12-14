from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django.urls import reverse_lazy

from . models import Election,Position,Candidates
from . form import Candidateapplyform
# Create your views here.

class DashboardView(TemplateView):

    template_name="election/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx["elections"]=Election.objects.filter(active=True) # Fetches only active elections from the database
        ctx["positions"]=Position.objects.select_related("election") #Fetches all positions Also fetches their related Election in the same database query
        return 
    



class CandinateApplyView(CreateView):
    model = Candidates
    template_name = "election/apply.html"
    form_class=Candidateapplyform
    success_url=reverse_lazy("election:dashboard")


    def form_valid(self, form):
        candinate = form.save(commit=False)
        candinate.user=self.request.user
        candinate.save()
        messages.success(self.request, "Application submitted.")
        return super().form_valid(form)

