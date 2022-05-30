from django.contrib import admin

from mainapp.models import Note, NoteShare, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at', 'updated_at', 'owner')
    
class NoteShareAdmin(admin.ModelAdmin):
    list_display = ('note', 'user')
    
admin.site.register(User, UserAdmin)
admin.site.register(Note, NotesAdmin)
admin.site.register(NoteShare, NoteShareAdmin)