from django.utils.translation import gettext_lazy as _


def is_authenticated(request):
    return request.user.is_authenticated


MENUS = {
    'MAIN_NAV': [
        {
            'name': _('Console'),
            'url': 'console:home',
            'icon_class': 'ft-terminal',
            'validators': ['core.menus.is_authenticated'],
        }
    ],
    'DROPDOWN_NAV': [
        {
            'name': _('Settings'),
            'url': 'auth:settings',
            'icon_class': 'ft-user',
            'validators': ['core.menus.is_authenticated'],
        },
        {
            'name': _('Logout'),
            'url': 'auth:logout',
            'separator': True,
            'icon_class': 'ft-log-out',
            'validators': ['core.menus.is_authenticated'],
        },

    ]
}
