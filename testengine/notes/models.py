from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class NoteManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id

        queryset = super(NoteManager, self).filter(content_type=content_type, object_id=object_id)
        return queryset


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    noted_item = GenericForeignKey('content_type', 'object_id')

    objects = NoteManager()
    
    def __str__(self):
        return f"{self.text} by {self.author} on {self.timestamp:%d-%m-%y %H:%M}"
