from django.urls import path

from . import views

app_name = 'testing'

urlpatterns = [
    path('list/', views.index, name='tests_index'),
    path('list/<str:slug>/', views.TestDetail.as_view(), name='test_detail_url'),
    path('questions/', views.QuestionsView.as_view(), name='questions_url'),
    path('questions/create/', views.QuestionCreate.as_view(), name='question_create_url'),
    path('questions/update/<int:id>/', views.QuestionUpdate.as_view(), name='question_update_url'),
    path('questions/delete/<int:id>/', views.QuestionDelete.as_view(), name='question_delete_url'),
    path('test/create/', views.TestCreate.as_view(), name='test_create_url'),
    path('test/delete/<int:id>/', views.TestDelete.as_view(), name='test_delete_url'),
    path('test/update/<int:id>/', views.TestUpdate.as_view(), name='test_update_url'),
    path('test/run/<int:id>/', views.TestRunAnswerView.as_view(), name='test_run_url'),
    path('test/run/<int:id>/list/', views.TestRunTestList.as_view(), name='test_run_test_list_url'),
    path('test/run/list/', views.TestRuns.as_view(), name='test_runs_url'),
    path('test/run/detail/<int:id>/', views.TestRunDetail.as_view(), name='test_run_detail_url'),
    path('add_note/', views.AddNoteView.as_view(), name='add_note_url'),
    
 ]