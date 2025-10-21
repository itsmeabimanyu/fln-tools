from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PDFMergeForm(forms.Form):
    pdf_files = forms.FileField(
        widget=MultipleFileInput(attrs={'id':'pdfs'}),
        label='Upload PDF files'
    )

class PDFSplitForm(forms.Form):
    pdf_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'id': 'pdfs'}),
        label='Upload PDF file',
    )
