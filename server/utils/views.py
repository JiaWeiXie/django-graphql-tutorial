from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


class ApolloSandboxView(LoginRequiredMixin, TemplateView):
    login_url = "/admin/login/"
    template_name = "sandbox.html"

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return csrf_exempt(view)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["graphql_url"] = self.request.build_absolute_uri("/graphql/")
        return context
