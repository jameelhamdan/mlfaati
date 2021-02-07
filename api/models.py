import binascii
import os
from django.utils.translation import gettext_lazy as _
from django.db import models


class Token(models.Model):
    """
    The authorization token model,
    Used custom model to allow more than one token per user
    """

    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tokens')
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def new_token(cls, user: 'users.User'):
        token = cls(user=user)
        token.save()
        return token

    def __str__(self):
        return self.key

    def short_key(self):
        key_length = int(len(self.key) / 2)
        return '%s...' % self.key[:key_length]

    class Meta:
        ordering = ['-key']
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')
        default_permissions = []
