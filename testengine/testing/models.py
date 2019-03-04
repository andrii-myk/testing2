from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

from notes.models import Note


class Question(models.Model):
    question = models.TextField(db_index=True)

    def __str__(self):
        return self.question
        
        
class Test(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank = True)
    questions = models.ManyToManyField('Question', related_name='tests')

    notes = GenericRelation(Note)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Test, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('testing:test_detail_url', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type


class TestRun(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    finished = models.DateTimeField(auto_now=True)
    
    notes = GenericRelation(Note)

    def __str__(self):
        return f"{self.test.title}, finished by user on {self.finished:%d-%m-%y %H:%M}"

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type


class TestRunAnswer(models.Model):
    answer = models.CharField(max_length=255)
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='testrunanswer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="testrun_answer")

    def __str__(self):
        return f"{self.question} and {self.answer}"
