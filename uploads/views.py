from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import media
import os
import time

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
        if file_obj.size > MAX_FILE_SIZE:
            return Response(
                {"error": f"File size cannot exceed {MAX_FILE_SIZE / 1024 / 1024}MB."},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        
        username = request.user.username
        original_filename = file_obj.name
        filename_base, file_extension = os.path.splitext(original_filename)
        # Get the current Unix timestamp
        timestamp = int(time.time())
        new_file_path = f"{username}/{filename_base}-{timestamp}{file_extension}"
        file_obj.name = new_file_path

        media_instance = media.objects.create(
            user=request.user,
            file=file_obj,
            original_filename=original_filename 
        )


        
        media_instance.save()

         # Here you would typically enqueue a background job to process the file
         # For example:
         # from .tasks import process_uploaded_file
         # process_uploaded_file.delay(media_instance.id)


        return Response(
            {"message": "File accepted and is being processed."},
            status=status.HTTP_202_ACCEPTED
        )
