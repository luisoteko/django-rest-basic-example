from django.shortcuts import render
from rest_framework import generics, permissions

from mainapp.serializers import NoteSerializer, NoteShareSerializer

# Create your views here.

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

class IsShared(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, NoteSerializer) and request.method == 'DELETE':
            return False
        if obj.shares.filter(user=request.user).exists():
            return True

class NotesView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = (IsOwner,)
    
class SharedNotesView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = (IsShared,)
    
class EditNoteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = (IsOwner, IsShared)

class ShareNoteView(generics.CreateAPIView):
    serializer_class = NoteShareSerializer
    permission_classes = (IsOwner,IsShared)
    
class ShareNoteDestroyView(generics.DestroyAPIView):
    serializer_class = NoteShareSerializer
    permission_classes = (IsOwner, IsShared)