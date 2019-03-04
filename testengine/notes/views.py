from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType

from .models import Note


class InstanceNotesListView(ListView):
    model = Note
    template_name = 'notes/base_notes.html'

    def get(self, request):
        obj = request.session.get('obj', None)
        mod = obj['model']
        ct = ContentType.objects.get(model=mod)
        notes = Note.objects.filter(content_type=ct)        
        return render(request, 'notes/notes.html', context={'notes': notes, 'model': mod})


class NotesListView(ListView):
    model = Note
    template_name = 'notes/notes.html'

    def get(self, request, model):
        ct = ContentType.objects.get(model=model)
        notes = Note.objects.filter(content_type=ct)        
        return render(request, 'notes/notes.html', context={'notes': notes, 'model': model})

    # def get_queryset(self):
    #     model = self.kwargs['content_type']
    #     content = ContentType.objects.get(model=model)
    #     return self.model.objects.filter(content_type=content.id)
