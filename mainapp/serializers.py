from rest_framework import serializers
from rest_registration.api.serializers import DefaultRegisterUserSerializer, DefaultUserProfileSerializer

from mainapp.models import Note, NoteShare, User

class NoteSerializer(serializers.ModelSerializer):
    shares = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'owner', 'shares']
        depth = 1
    def get_shares(self, obj):
        return NoteShareSerializer(obj.shares.all(), many=True).data 

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__' 

class NoteShareSerializer(serializers.ModelSerializer):
    showed_name = serializers.SerializerMethodField()
    class Meta:
        model = NoteShare
        fields = '__all__'
    def get_showed_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name} - {obj.user.email}'
        

class UserSerializer(DefaultUserProfileSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class RegisterSerializer(DefaultRegisterUserSerializer):
    class Meta:
        model = User
