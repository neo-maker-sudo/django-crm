from django.urls import path
from . import views

urlpatterns = [
    path("list", views.LeadsListView.as_view(), name="leads_list"),
    path("<int:pk>/detail", views.LeadsDetailView.as_view(), name="leads_detail"),
    path("create", views.LeadsCreateView.as_view(), name="leads_create"),
    path("<int:pk>/update", views.LeadsUpdateView.as_view(), name="leads_update"),
    path("<int:pk>/delete", views.LeadsDeleteView.as_view(), name="leads_delete"),
    path("<int:pk>/assign/agent", views.AgentAssignView.as_view(), name="leads_assign_agent"),
    # path("list", views.leads_list_view, name="leads_list"),
    # path("<int:pk>/detail", views.leads_detail_view, name="leads_detail"),
    # path("create", views.leads_create_view, name="leads_create"),
    # path("<int:pk>/update", views.leads_update_view, name="leads_update"),
    # path("<int:pk>/delete", views.leads_delete_view, name="leads_delete"),
]
