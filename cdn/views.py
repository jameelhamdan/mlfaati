from urllib.parse import quote
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.http import FileResponse, HttpResponse
import core.models


class BaseServeView(SingleObjectMixin, View):
    queryset = core.models.File.objects.select_related('folder', 'space')

    def get_object(self, queryset=None) -> 'core.models.File':
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        file = self.object.content
        file_name = self.object.name
        file_path = self.object.content.url

        if settings.DEBUG:
            # Serve through normal HTTP in debug mode
            return FileResponse(file, as_attachment=False, filename=file_name)

        # Serve through Nginx in production
        response = HttpResponse()
        try:
            file_name.encode('ascii')
            file_expr = 'filename="{}"'.format(file_name)
        except UnicodeEncodeError:
            file_expr = "filename*=utf-8''{}".format(quote(file_name))

        response['content-disposition'] = 'attachment; %s' % file_expr

        try:
            file_path.encode('ascii')
        except UnicodeEncodeError:
            file_path = quote(file_path)

        response['content_type'] = self.object.content_type
        # Nginx header for proxying files
        response['X-Accel-Redirect'] = file_path
        return response


class ServeByPathView(BaseServeView):
    def get_object(self, queryset=None):
        path_list = self.kwargs['path'].split(core.models.PATH_CONCAT_CHARACTER)
        if len(path_list) == 0:
            raise core.models.File.DoesNotExist()

        file_name = path_list.pop()
        qs = self.get_queryset()

        if len(path_list) > 0:
            qs = qs.filter(folder__path__exact=path_list)
        else:
            qs = qs.filter(folder__isnull=True)

        return get_object_or_404(
            qs, name=file_name, space__name__exact=self.kwargs['space_name']
        )


class ServeByIdView(BaseServeView):
    def get_object(self, queryset=None):
        space_name = self.kwargs.get('space_name')
        if space_name:
            return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'], space__name__exact=space_name)
        return super().get_object(queryset=queryset)
