from django.http.response import Http404
from django.views import generic
from django.urls import reverse_lazy
from django.views.static import serve
from . import DOCS_ROOT


class ServeView(generic.View):
    def get(self, request, *args, **kwargs):
        kwargs['document_root'] = DOCS_ROOT

        try:
            return serve(request, **kwargs)
        except Http404:
            raise


class RootView(generic.RedirectView):
    permanent = False
    url = reverse_lazy('docs:files', kwargs={'path': 'index.html'})
