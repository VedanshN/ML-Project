from django.conf import settings
from .models import Document, DocumentAnalysis
import openai
import json

# To handle different file types, you'll need to install specific libraries.
# For PDFs: pip install pypdf2
# For DOCX: pip install python-docx


class DocumentAnalysisService:
    """
    A service class to encapsulate the business logic for analyzing documents
    using the OpenAI API.
    """

    def __init__(self, document: Document):
        if not isinstance(document, Document):
            raise TypeError("A valid Document object must be provided.")
        self.document = document

        # Configure OpenAI client
        if not hasattr(settings, 'OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY is not configured in your project settings.")
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def _extract_text(self) -> str:
        """
        Extracts text content from the document file based on its extension.
        This supports .txt, .pdf, and .docx files.
        """
        try:
            # The file object needs to be opened to read its content
            with self.document.file.open('rb') as f:
                filename = self.document.file.name
                if filename.endswith('.txt'):
                    return f.read().decode('utf-8')


        except Exception as e:
            print(f"Error extracting text from {self.document.original_filename}: {e}")
            return ""  # Return empty string on error

    def analyze(self):
        """
        Runs the document analysis process using the OpenAI API.
        """
        try:
            # 1. Update status to PROCESSING
            self.document.status = Document.UploadStatus.PROCESSING
            self.document.save()

            # --- EXTRACT TEXT FROM DOCUMENT ---
            print(f"Starting text extraction for {self.document.original_filename}...")
            document_content = self._extract_text()
            if not document_content or document_content.startswith("Unsupported"):
                raise ValueError(document_content or "Text could not be extracted from the document.")

            # --- CALL OPENAI API FOR ANALYSIS ---
            print("Sending content to OpenAI for analysis...")
            prompt = f"""
            Analyze the following document text and provide a structured JSON response.
            The JSON object must contain three keys:
            1. "summary": A concise summary of the document.
            2. "key_phrases": A list of 5-10 important keywords or phrases.
            3. "sentiment": The overall sentiment of the text (e.g., "positive", "negative", "neutral").

            Document Text:
            ---
            {document_content[:8000]}
            ---

            Provide only the raw JSON object as your response.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini", # A cost-effective and powerful model
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are an expert document analyst that always responds with valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            analysis_results = json.loads(response.choices[0].message.content)

            # 2. Store the results from OpenAI
            DocumentAnalysis.objects.update_or_create(
                document=self.document,
                defaults={
                    'summary': analysis_results.get("summary", "No summary generated."),
                    'key_phrases': analysis_results.get("key_phrases", []),
                    'sentiment': analysis_results.get("sentiment", "unknown"),
                }
            )

            # 3. Update status to COMPLETED
            self.document.status = Document.UploadStatus.COMPLETED
            self.document.save()
            print("Analysis finished and results saved.")
            return True, "Analysis completed successfully."

        except Exception as e:
            # 4. Update status to FAILED on error
            self.document.status = Document.UploadStatus.FAILED
            self.document.save()
            error_message = f"An error occurred: {e}"
            print(f"Error analyzing document {self.document.id}: {error_message}")
            # Optionally save the error to the analysis object
            DocumentAnalysis.objects.update_or_create(
                document=self.document,
                defaults={'summary': f"Analysis Failed: {error_message}"}
            )
            return False, error_message


def start_document_analysis(document_id: str):
    """
    Initiates the analysis for a given document ID.
    This function is ideal for calling from a background task runner like Celery.
    """
    try:
        document = Document.objects.get(id=document_id)
        service = DocumentAnalysisService(document)
        service.analyze()
    except Document.DoesNotExist:
        print(f"Document with ID {document_id} not found.")

