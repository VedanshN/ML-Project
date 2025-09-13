import uuid
from django.db import models
from django.conf import settings

# It's good practice to get the User model from settings
# in case it has been customized.
User = settings.AUTH_USER_MODEL

class Document(models.Model):
    """
    Represents an uploaded document in the system.
    """
    class UploadStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        UPLOADING = 'UPLOADING', 'Uploading'
        UPLOADED = 'UPLOADED', 'Uploaded'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    file = models.FileField(upload_to='uploaded_documents/')
    original_filename = models.CharField(max_length=255)
    filesize = models.PositiveIntegerField(help_text="Size in bytes")
    status = models.CharField(max_length=20, choices=UploadStatus.choices, default=UploadStatus.PENDING)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Document {self.original_filename} by {self.user.username if self.user else 'Anonymous'}"

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Document"
        verbose_name_plural = "Documents"

class DocumentAnalysis(models.Model):
    """
    Stores the results of the analysis for a given document.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='analysis')
    summary = models.TextField(blank=True, null=True)
    key_phrases = models.JSONField(blank=True, null=True) # Requires PostgreSQL or modern SQLite
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.document.original_filename}"

    class Meta:
        verbose_name = "Document Analysis"
        verbose_name_plural = "Document Analyses"
