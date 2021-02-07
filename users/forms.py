from crispy_forms.bootstrap import PrependedText
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, ButtonHolder, Submit
from django.contrib.auth import forms as auth_forms
from common.crispy import Anchor
from . import models


class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Remember me'), initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-vertical remove-asterisk'
        self.helper.layout = Layout(
            Div(
                Field(
                    PrependedText(
                        'username', mark_safe('<i class="ft-mail"></i>'),
                        placeholder=_('example@company.com'), wrapper_class='col-12')
                ),
                Field(
                    PrependedText(
                        'password', mark_safe('<i class="ft-unlock"></i>'),
                        placeholder=_('Password'), wrapper_class='pt-4 col-12'
                    )
                ),
                Div(
                    Field(
                        'remember_me', placeholder=_('Remember me'),
                        css_class='form-check-input'
                    ),
                    Anchor(
                        url='#',  # TODO: make forget password page
                        text=_('Lost password?'),
                        css_class='small text-right',
                    ),
                    css_class='d-flex justify-content-between align-items-top pt-4 col-12'
                ),
                ButtonHolder(
                    Submit('submit', _('Sign in'), css_class='w-100'),
                    css_class='pt-4 col-12'
                ),
                css_class='row'
            )
        )


class SettingsForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-vertical remove-asterisk'
        self.helper.layout = Layout(
            Div(
                Field('first_name', wrapper_class='col-6'),
                Field('last_name', wrapper_class='col-6'),
                ButtonHolder(
                    Submit('submit', _('Save')),
                    css_class='pt-4 col-12'
                ),
                css_class='row'
            )
        )
