from typing import Optional
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import (
    ListView, DetailView, FormView,
    CreateView, UpdateView, DeleteView, 
)
from .models import Lead
from .forms import LeadForm, AssignAgentForm
from base.mixins import CustomLoginRequiredMixin


class LeadsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    template_name: str = "leads/leads_list.html"
    context_object_name: Optional[str] = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.organization).order_by("-agent", "id")
        else:
            queryset = Lead.objects.filter(agent__user=user).order_by("-agent", "id")

        return queryset


class LeadsDetailView(CustomLoginRequiredMixin, DetailView):
    login_url = reverse_lazy("login")
    template_name: str = "leads/leads_detail.html"
    context_object_name: Optional[str] = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(agent__user=user)

        return queryset


class LeadsCreateView(CustomLoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    template_name: str = "leads/leads_create.html"
    form_class = LeadForm
    success_url: Optional[str] = reverse_lazy("leads_list") 

    def form_valid(self, form: LeadForm) -> HttpResponse:
        new_lead = form.save(commit=False)
        new_lead.organization = self.request.user.organization
        new_lead.save()

        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )
        return super().form_valid(form)


class LeadsUpdateView(CustomLoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    template_name: str = "leads/leads_update.html"
    form_class = LeadForm
    success_url: Optional[str] = reverse_lazy("leads_list")

    def get_queryset(self):
        # initial queryset of leads for the entire organisation
        return Lead.objects.select_related(
            "agent", "category", "organization"
        ).filter(organization=self.request.user.organization)


class LeadsDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Lead
    success_url: Optional[str] = reverse_lazy("leads_list")
    
    def get(self, request, pk):
        return redirect(reverse("leads_list"))


class AgentAssignView(CustomLoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    success_url: Optional[str] = reverse_lazy("leads_list")
    template_name: str = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)

        kwargs.update({
            "request": self.request,

        })
        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            lead = Lead.objects.get(id=self.kwargs["pk"])
        except Lead.DoesNotExist:
            return redirect(reverse("login"))
        
        context.update({
            "lead": lead
        })

        return context 

    def form_valid(self, form: AssignAgentForm) -> HttpResponse:
        agent = form.cleaned_data["agent"]
        
        try:
            lead = Lead.objects.get(id=self.kwargs["pk"])
            lead.agent = agent
            lead.save()
        except Lead.DoesNotExist:
            return redirect(reverse("login"))

        return super().form_valid(form)