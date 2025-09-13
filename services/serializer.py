from rest_framework import serializers
from .models import Document, DocumentAnalysis

class DocumentAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for the DocumentAnalysis results."""
    class Meta:
        model = DocumentAnalysis
        fields = ['id', 'summary', 'key_phrases', 'sentiment', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for the Document model."""
    analysis = DocumentAnalysisSerializer(read_only=True)
    user = serializers.StringRelatedField() # Display user's string representation

    class Meta:
        model = Document
        fields = [
            'id',
            'user',
            'file',
            'original_filename',
            'filesize',
            'status',
            'uploaded_at',
            'processed_at',
            'analysis'
        ]
        read_only_fields = [
            'id',
            'user',
            'original_filename',
            'filesize',
            'status',
            'uploaded_at',
            'processed_at',
            'analysis'
        ]

    def create(self, validated_data):
        # Add the user from the request context
        user = self.context['request'].user
        file_obj = validated_data['file']

        # Create the document instance
        document = Document.objects.create(
            user=user,
            file=file_obj,
            original_filename=file_obj.name,
            filesize=file_obj.size,
            status=Document.UploadStatus.UPLOADED # Set status after upload
        )
        return document
