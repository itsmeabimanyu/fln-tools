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
            'placeholder': 'Enter your text here',
            'autocomplete': 'off'
        })
    )
    with_icon = forms.BooleanField(
        label='QR code generator with logo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'})
    )

BARCODE_CHOICES = [
    ('code39', 'Code 39'),
    ('code39_mod43', 'Code 39 Mod 43'),
    ('code128', 'Code 128'),
    ('ean13', 'EAN-13'),
    ('ean8', 'EAN-8'),
    ('isbn10', 'ISBN-10'),
    ('isbn13', 'ISBN-13'),
    ('issn', 'ISSN'),
    ('upc', 'UPC-A'),
]

class BarcodeForm(forms.Form):
    data = forms.CharField(
        label='Data untuk Barcode',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',  # class untuk styling, misalnya Bootstrap
            'placeholder': 'Enter your text here',
            'autocomplete': 'off'
        })
    )
    
    barcode_type = forms.ChoiceField(
        choices=[('', 'Select Barcode Type')] + BARCODE_CHOICES,
        label='Tipe Barcode',
        widget=forms.Select(attrs={
            'class': 'form-control form-select mb-3'  # class untuk dropdown styling
        })
    )

QUALITY_CHOICES = [
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
]

class PDFCompressForm(forms.Form):
    pdf_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'id': 'pdfs'}),
        label='Upload PDF file',
    )
    
    quality = forms.ChoiceField(
        choices=[('', 'Select Compression Level')] + QUALITY_CHOICES, 
        initial='medium', 
        label="Compression Level", 
        widget=forms.Select(attrs={
            'class': 'form-control form-select mb-3'
        })
    )

