from django.db import models

class PublishManager(models.Manager):

    def get_queryset(self):
        queryset = super(PublishManager, self).get_queryset().filter(
            status='published')

        return queryset


class DraftManager(models.Manager):

    def get_queryset(self):
        queryset = super(DraftManager, self).get_queryset().filter(
            status='draft')

        return queryset
