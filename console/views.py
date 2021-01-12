from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from sql_util.utils import SubquerySum, SubqueryCount
from common.views import PageMixin
import core.models
from console import forms


class HomeView(PageMixin, generic.ListView):
    template_name = 'console/home.html'
    page_title = _('Console')
    context_object_name = 'spaces_list'
    extra_context = {
        'PRIVACY': core.models.Space.PRIVACY.as_dict()
    }
    breadcrumbs = [
        (_('Console'), '#'),
    ]

    def get_queryset(self):
        return core.models.Space.objects.owned(self.request.user).annotate(
            files_count=SubqueryCount('files'),
            files_total_size=SubquerySum('files__content_length'),
        )


class BrowseView(PageMixin, generic.DetailView):
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


class CreateSpaceView(PageMixin, generic.CreateView):
    template_name = 'console/space/form.html'
    form_class = forms.SpaceForm
    page_title = _('Console - Add Space')
    context_object_name = 'space'
    success_url = _('Added Space.')

    def get_breadcrumbs(self):
        return [
            (_('Console'), reverse_lazy('console:home')),
            (_('Add Space'), '#'),
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cancel_url'] = reverse_lazy('console:home')
        return kwargs

    def get_success_url(self):
        return reverse_lazy('console:space_browse', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateSpaceView, self).form_valid(form)


class UpdateSpaceView(PageMixin, generic.UpdateView):
    template_name = 'console/space/form.html'
    form_class = forms.SpaceForm
    page_title = _('Console - Update %s Space')
    context_object_name = 'space'
    success_url = _('Updated Space.')

    def get_queryset(self):
        return core.models.Space.objects.owned(self.request.user)

    def get_page_title(self):
        return self.page_title % str(self.object)

    def get_breadcrumbs(self):
        return [
            (_('Console'), reverse_lazy('console:home')),
            (self.object, reverse_lazy('console:space_browse', kwargs={'pk': self.object.pk})),
            (_('Update'), '#'),
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cancel_url'] = reverse_lazy('console:space_browse', kwargs={'pk': self.object.pk})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('console:space_update', kwargs={'pk': self.object.pk})
