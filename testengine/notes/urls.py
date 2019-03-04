from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('<str:model>/', views.NotesListView.as_view(), name='notes_url'),
    path('', views.InstanceNotesListView.as_view(), name='instance_notes_url'),
    
 ]