from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import DetailView
from sql_util.utils import SubquerySum, SubqueryCount
from common.views import PageMixin
import core.models


class HomeView(PageMixin, generic.ListView):
    template_name = 'console/home.html'
    page_title = _('Console')
    context_object_name = 'spaces_list'
    breadcrumbs = [
        (_('Console'), '#'),
    ]

    def get_queryset(self):
        return core.models.Space.objects.owned(self.request.user).annotate(
            files_count=SubqueryCount('files'),
            files_total_size=SubquerySum('files__content_length'),
        )


class BrowseView(PageMixin, DetailView):
    template_name = 'console/browser.html'
    page_title = _('Console - %s Space')
    context_object_name = 'space'

    def get_queryset(self):
        return core.models.Space.objects.owned(self.request.user).annotate(
            files_count=SubqueryCount('files'),
            files_total_size=SubquerySum('files__content_length'),
        )

    def get_page_title(self):
        return self.page_title % str(self.object)

    def get_breadcrumbs(self):
        return [
            (_('Console'), reverse_lazy('console:home')),
            (self.object, '#'),
        ]
