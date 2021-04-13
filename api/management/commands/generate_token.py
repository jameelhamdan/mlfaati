from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from users.models import User
from api.models import Token


class Command(BaseCommand):
    help = 'Generate API token for provided user'

    def add_arguments(self, parser):
        parser.add_argument(
            'email', help='Email to generate token for', type=str
        )

    def handle(self, *args, **options):
        username = options['email']

        try:
            u = User.objects.get(email=username)
        except User.DoesNotExist:
            raise CommandError("user '%s' does not exist" % username)

        token = Token.new_token(u)

        self.stdout.write(f'New Token for %s is: %s' % (username, token.key))
