from typing import Optional
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView, 
    CreateView, UpdateView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from base.models import User
from .forms import AgentForm
from base.mixins import CustomLoginRequiredMixin


class AgentsListView(CustomLoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    template_name: str = "agents/agents_list.html"
    context_object_name: Optional[str] = "agents"
    
    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)
    
    
    
class AgentsCreateView(CustomLoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    template_name: str = "agents/agents_create.html"
    form_class = AgentForm
    success_url: Optional[str] = reverse_lazy("agents:list")
    
    def form_valid(self, form: AgentForm):
        # user model
        username = form.cleaned_data.get("username")
        new_user = form.save(commit=False)
        new_user.is_agent = True
        new_user.is_organisor = False
        new_user.set_password(username)
        new_user.save()
        
        # agent model
        Agent.objects.create(
            user=new_user,
            organization=self.request.user.organization
        )
        
        return super().form_valid(form)


class AgentsDetailView(CustomLoginRequiredMixin, DetailView):
    login_url = reverse_lazy("login")
    template_name: str = "agents/agents_detail.html"
    context_object_name: Optional[str] = "agent"

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)


class AgentsUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    template_name: str = "agents/agents_update.html"
    form_class = AgentForm
    success_url: Optional[str] = reverse_lazy("agents:list")

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

    def form_valid(self, form: AgentForm):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        
        agent = form.save(commit=False)
        
        agent.user.username = username
        agent.user.email = email
        agent.user.first_name = first_name
        agent.user.last_name = last_name
        agent.user.save()

        return super().form_valid(form)


class AgentsDeleteView(CustomLoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Agent
    success_url: Optional[str] = reverse_lazy("agents:list")

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

    def get(self, request, pk):
        return redirect(reverse("agents:list"))