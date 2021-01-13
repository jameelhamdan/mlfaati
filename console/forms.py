from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, ButtonHolder, Submit
from django import forms
import core.models
from common.crispy import Anchor


class SpaceForm(forms.ModelForm):
    class Meta:
        model = core.models.Space
        fields = ['name', 'privacy']

    def __init__(self, cancel_url, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-vertical'
        self.helper.layout = Layout(
            Div(
                Field('name', placeholder=_('Unique space name'), wrapper_class='pt-3 col-12 col-md-6'),
                Field('privacy', wrapper_class='pt-3 col-12 col-md-6'),
                ButtonHolder(
                    Submit('submit', _('Save')),
                    Anchor(cancel_url, _('Cancel')),
                    css_class='pt-3 col-12'
                ),
                css_class='row'
            )
        )
