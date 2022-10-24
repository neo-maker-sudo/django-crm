from typing import Optional
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from leads.models import Lead
from .models import Category
from .forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    template_name: str = "category/categories_list.html"
    context_object_name = "categories"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update({
            "unassigned_count": queryset.filter(category__isnull=True).count()
        })
    
        return context

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset


class CategoryCreateView(LoginRequiredMixin, CreateView):
    template_name: str = "category/categories_create.html"
    login_url = reverse_lazy("login")
    form_class = CategoryForm
    success_url: Optional[str] = reverse_lazy("categories_list") 


    def form_valid(self, form: CategoryForm):
        
        if self.request.user.is_organisor:
            category = form.save(commit=False)
            
            category.organization = self.request.user.organization
            category.save()
        
        
        return super().form_valid(form)


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name: str = "category/categories_detail.html"
    context_object_name = "category"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        leads = self.get_object().leads.filter(
            organization=self.request.user.organization
        )

        context.update({
            "leads": leads    
        })
        
        return context   

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
        
        return queryset


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    template_name: str = "category/categories_update.html"
    form_class = CategoryForm
    success_url: Optional[str] = reverse_lazy("categories_list")

    def get_queryset(self):
        
        return Category.objects.select_related(
          "organization"
        ).filter(organization=self.request.user.organization)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Category
    success_url: Optional[str] = reverse_lazy("categories_list")
    
    def get(self, request, pk):
        print("dsadasdas ???")
        return redirect(reverse("categories_list"))
