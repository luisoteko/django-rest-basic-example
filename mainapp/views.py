from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics, permissions
from mainapp.models import Note, NoteShare, User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from mainapp.serializers import NoteSerializer, NoteShareSerializer

# Create your views here.

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, NoteSerializer) or isinstance(obj, Note):
            if obj.owner == request.user:
                return True
        if obj.user == request.user:
            return True

class IsShared(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (isinstance(obj, NoteSerializer) or isinstance(obj, Note)) and request.method == 'DELETE':
            return False
        if obj.user == request.user:
            return True

class NotesView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
    
    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        print(request.data['owner'])
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        return super().post(request, *args, **kwargs)
    
class SharedNotesView(generics.ListAPIView):
    serializer_class = NoteSerializer
    def get_queryset(self):
        return Note.objects.filter(shares__user=self.request.user)
    
@csrf_exempt
@api_view(['POST'])
def createShare(request, *args, **kwargs):
    email = request.data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'email': 'User does not exist'})
    try:
        note = Note.objects.get(id=request.data['note'])
    except IntegrityError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'email': 'Already shared with this user'})
    share = NoteShare.objects.create(user=user, note=note)
    data = NoteShareSerializer(share).data
    return Response(status=status.HTTP_201_CREATED, data=data)
class EditNoteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsOwner | IsShared]
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user) | Note.objects.filter(shares__user=self.request.user)
    

class ShareNoteView(generics.CreateAPIView):
    serializer_class = NoteShareSerializer
    permission_classes = [IsOwner | IsShared]
    
class ShareNoteDestroyView(generics.DestroyAPIView):
    serializer_class = NoteShareSerializer
    def get_queryset(self):
        return NoteShare.objects.filter(note__owner=self.request.user) | NoteShare.objects.filter(user=self.request.user)