import os, zipfile, qrcode, base64
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.utils.text import slugify
from django.views.generic import (
    TemplateView
)
from .forms import (
    PDFMergeForm, PDFSplitForm, QRCodeForm
)
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from PIL import Image

# Create your views here.
class PDFMerge(TemplateView):
    template_name = 'pages/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Merge PDF'
        context['subtitle'] = 'Please upload at least two PDF files that you want to merge into a single document.'
        context['form'] = PDFMergeForm()
        context['buttons_action'] = [
                f'''
                <button type="submit" name="action" value="merge" class="btn-primary">
                                    <span>Submit</span>
                                    <i class="bi bi-arrow-right-circle"></i>
                                   </button>
                '''
            ]
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        referer = request.META.get('HTTP_REFERER', '/')

        if action == 'merge':
            files = request.FILES.getlist('pdf_files')
            
            if files:
                writer = PdfWriter()

                for f in files:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        writer.add_page(page)

                merged_pdf = BytesIO()
                writer.write(merged_pdf)
                merged_pdf.seek(0)

                # Ambil nama file pertama sebagai dasar nama hasil
                first_filename = files[0].name
                base_name = os.path.splitext(first_filename)[0]
                merged_filename = f"{base_name}_merged.pdf"

                response = HttpResponse(merged_pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{merged_filename}"'
                return response

        return redirect(referer)

class PDFSplit(TemplateView):
    template_name = 'pages/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Split PDF'
        context['subtitle'] = 'Please upload a PDF file that you want to split into separate pages or sections.'
        context['form'] = PDFSplitForm()
        context['buttons_action'] = [
                f'''
                <button type="submit" name="action" value="split" class="btn-primary">
                                    <span>Submit</span>
                                    <i class="bi bi-arrow-right-circle"></i>
                                   </button>
                '''
            ]
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        referer = request.META.get('HTTP_REFERER', '/')

        if action == 'split':
            file = request.FILES.get('pdf_file')

            try:
                # Ambil nama file asli tanpa ekstensi
                original_filename = file.name
                base_filename = os.path.splitext(original_filename)[0]  # contoh: 'laporan_akhir'

                reader = PdfReader(file)
                zip_buffer = BytesIO()

                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for i, page in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(page)

                        pdf_bytes = BytesIO()
                        writer.write(pdf_bytes)
                        pdf_bytes.seek(0)

                        filename = f'page-{i+1}.pdf'
                        zip_file.writestr(filename, pdf_bytes.read())

                zip_buffer.seek(0)
                zip_filename = f"{base_filename}.zip"

                response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
                return response

            except Exception as e:
                messages.error(request,"PDF processing error:", e)
                return redirect(referer)

from django.conf import settings

class QRCodeGenerator(TemplateView):
    template_name = 'pages/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'QR Code Generator'
        context['subtitle'] = 'Input text, URL, or any information to create its QR Code.'
        context['form'] = QRCodeForm()
        context['buttons_action'] = [
                f'''
                <button type="submit" name="action" value="generate" class="btn-primary">
                                    <span>Submit</span>
                                    <i class="bi bi-arrow-right-circle"></i>
                                   </button>
                '''
            ]
        return context
    
    def post(self, request, *args, **kwargs):
        form = QRCodeForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            data = form.cleaned_data['data']
            with_icon = form.cleaned_data.get('with_icon', False)  # Ambil nilai checkbox

            # Generate QR Code seperti biasa
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            if with_icon:
                # Jika checkbox dicentang, tambahkan logo
                logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_01.jpg')
                logo = Image.open(logo_path)

                logo_size = int(img_qr.size[0] * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

                pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)

                if logo.mode == 'RGBA':
                    img_qr.paste(logo, pos, mask=logo)
                else:
                    img_qr.paste(logo, pos)

            # Encode ke base64
            buffer = BytesIO()
            img_qr.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            img_data = f"data:image/png;base64,{img_str}"

            context['code_img'] = img_data
            context['text'] = data
            context['filename'] = slugify(data)

        context['form'] = form
        return render(request, self.template_name, context)