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

class QRCodeForm(forms.Form):
    data = forms.CharField(
        label='Data untuk QR Code',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',  # class untuk styling, misalnya Bootstrap
            'placeholder': 'Enter your text here'
        })
    )
    with_icon = forms.BooleanField(
        label='QR code generator with logo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'})
    )
