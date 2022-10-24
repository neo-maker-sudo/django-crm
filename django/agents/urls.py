from django.urls import path
from . import views

app_name = "agents"

urlpatterns = [
    path("list", views.AgentsListView.as_view(), name="list"),
    path("create", views.AgentsCreateView.as_view(), name="create"),
    path("<int:pk>/detail", views.AgentsDetailView.as_view(), name="detail"),
    path("<int:pk>/update", views.AgentsUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.AgentsDeleteView.as_view(), name="delete"),
]
