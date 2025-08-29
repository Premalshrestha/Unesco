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
# forms.py
from django import forms
from .models import Discussion, Reply, Category

class DiscussionForm(forms.ModelForm):
    """Form for creating/editing discussions"""
    
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'category', 'priority', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter discussion title...',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe your question or topic in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., python, web-development, django)',
                'help_text': 'Tags help others find your discussion'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category required and add empty option
        self.fields['category'].empty_label = "Select a category"
        self.fields['category'].required = True
        
        # Add helpful labels
        self.fields['title'].label = "Discussion Title"
        self.fields['content'].label = "Description"
        self.fields['priority'].label = "Priority Level"
        self.fields['tags'].label = "Tags (Optional)"
        
        # Add help text
        self.fields['content'].help_text = "Please provide as much detail as possible to help others understand your question or topic."
        self.fields['priority'].help_text = "How urgent is this discussion?"

class ReplyForm(forms.ModelForm):
    """Form for adding replies to discussions"""
    
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts, suggestions, or solutions...',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = "Your Reply"
        self.fields['content'].help_text = "Be constructive and helpful in your response."

class SearchForm(forms.Form):
    """Form for searching discussions"""
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search discussions, content, or tags...',
            'autocomplete': 'off'
        }),
        required=False
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Discussion.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Discussion.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    user_type = forms.ChoiceField(
        choices=[('', 'All Users'), ('user', 'Regular Users'), ('consultant', 'Consultants')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="Posted by"
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('latest', 'Latest'),
            ('popular', 'Most Viewed'),
            ('replies', 'Most Replies'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        initial='latest'
    )