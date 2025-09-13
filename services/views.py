from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Document
from .serializer import DocumentSerializer
from .services import start_document_analysis
import threading

class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows documents to be viewed or uploaded.
    """
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'delete'] # Disallow PUT/PATCH

    def get_queryset(self):
        """
        This view should return a list of all the documents
        for the currently authenticated user.
        """
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handle file upload and trigger the analysis in the background.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The serializer's create method handles saving the file
        # and associating the user.
        document = serializer.save()

        # --- Trigger Analysis in a Background Thread ---
        # In a production environment, you should use a proper task queue
        # like Celery instead of a simple thread.
        analysis_thread = threading.Thread(
            target=start_document_analysis,
            args=(document.id,)
        )
        analysis_thread.start()
        # --- End of Background Task Trigger ---

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
