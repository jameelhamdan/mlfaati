from django.utils.translation import gettext_lazy as _


def is_authenticated(request):
    return request.user.is_authenticated


MENUS = {
    'MAIN_NAV': [
        {
            'name': _('Console'),
            'url': 'console:Home',  # reversible
            'icon_class': 'ft-terminal',
            'validators': ['core.menus.is_authenticated'],
        }
    ],
}
