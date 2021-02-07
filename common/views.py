class BreadcrumbsMixin:
    """
    This will handle building and passing breadcrumbs to view
    """
    breadcrumbs = []  # List of tuples (title, href)

    def get_breadcrumbs(self):
        return self.breadcrumbs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = self.get_page_title()
        return context


class PageMixin(PageTitleMixin, BreadcrumbsMixin):
    """
    Generic mixin to apply all mixins in one mixin
    """
    page_title = None
