# /app/uploads/serializer.py

from rest_framework import serializers
from .models import media 

class FileUploadSerializer(serializers.ModelSerializer):
    """
    A clean, production-ready serializer for the media model.
    It handles file uploads and correctly returns the full file URL.
    """
    # The 'description' field is accepted from the frontend but not saved to the model.
    description = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = media
        # The 'file' field will handle the file upload on input.
        # The 'to_representation' method below will handle generating the full URL on output.
        fields = ['id', 'file', 'uploaded_at', 'description']
        read_only_fields = ('id', 'uploaded_at')

    def create(self, validated_data):
        """
        Overrides the default create method to handle the extra 'description' field.
        """
        # Remove the 'description' field before creating the model instance.
        validated_data.pop('description', None)
        
        instance = media.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        """
        Overrides the default representation to ensure the 'file' field
        is always a full, absolute URL. This is the most reliable way to fix
        the 'undefined' URL issue on the frontend.
        """
        # Get the default representation from the parent class.
        representation = super().to_representation(instance)
        
        # Check if the instance has a file and if that file has a .url attribute.
        # The .url attribute is provided by the storage backend (local or GCS).
        if instance.file and hasattr(instance.file, 'url'):
            # Replace the default file path with the full, absolute URL.
            representation['file'] = instance.file.url
            
        return representation
