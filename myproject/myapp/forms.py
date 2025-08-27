#

from django import forms
from .models import UploadedDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['document']
        widgets = {
            'document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            })
        }
    
    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            if not document.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            if document.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('File size must be less than 10MB.')
        return document
