from django.urls import path
from . import views

urlpatterns = [
    path("list", views.CategoryListView.as_view(), name="categories_list"),
    path("create", views.CategoryCreateView.as_view(), name="categories_create"),
    path("<int:pk>/delete", views.CategoryDeleteView.as_view(), name="categories_delete"),
    path("<int:pk>/detail", views.CategoryDetailView.as_view(), name="categories_detail"),
    path("<int:pk>/update", views.CategoryUpdateView.as_view(), name="categories_update"), 

    
]
