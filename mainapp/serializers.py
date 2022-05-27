from rest_framework import serializers

from mainapp.models import Note, NoteShare

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteShare
        fields = '__all__'