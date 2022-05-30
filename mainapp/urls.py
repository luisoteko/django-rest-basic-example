from django.urls import include, path
from mainapp import views

urlpatterns = [
    path('notes/', views.NotesView.as_view()),
    path('notes/<int:pk>/', views.EditNoteView.as_view()),
    path('notes/shared/', views.SharedNotesView.as_view()),
    path('shares/<int:pk>/', views.ShareNoteDestroyView.as_view()),
    path('share/', views.createShare),
    path('shares/<int:pk>/', views.ShareNoteDestroyView.as_view()),
]
