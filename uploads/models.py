# /app/uploads/models.py

from django.db import models
import uuid
from django.conf import settings

class media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    original_filename = models.CharField(max_length=255, default='original_filename.mp4')
    
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media'
        ordering = ['-uploaded_at']

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.original_filename}"
        return f"Anonymous - {self.original_filename}"

