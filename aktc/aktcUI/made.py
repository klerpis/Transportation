from django.db import models


class BookDate(models.DateField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ''


class BookDate(models.Model):
    ''
