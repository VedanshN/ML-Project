from django.contrib import admin
from .models import media

admin.site.register(media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'uploaded_at')
    list_filter = ('uploaded_at')
    search_fields = ('id', 'User', 'file')
