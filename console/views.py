from django.utils.translation import gettext_lazy as _
from django.views import generic
from common.views import PageMixin


class HomeView(PageMixin, generic.TemplateView):
    template_name = 'console/home.html'
    page_title = _('Console')
    breadcrumbs = [
        (_('Console'), '#'),
    ]
