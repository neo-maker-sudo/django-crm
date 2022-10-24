from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin


class CustomLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user.is_authenticated and not request.user.is_organisor:
            return redirect(reverse("leads_list"))
        
        return super().dispatch(request, *args, **kwargs)