from crispy_forms.layout import TEMPLATE_PACK, Field
from django.template import Template, Context


class Anchor:
    context = {}
    html_template = '<a href="{{ url }}" class="{{ css_class }}" {% if css_id %}id="{{ css_id }}"{% endif %}>{{text}}</a>'

    def __init__(self, url, text, css_class="btn btn-outline-warning", css_id=None, **kwargs):
        self.context = {
            'url': url,
            'text': text,
            'css_class': css_class,
            'css_id': css_id
        }

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return Template(str(self.html_template)).render(Context(self.context))
