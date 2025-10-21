# Django imports
from django.urls import path
from django.shortcuts import redirect
# Project-specific imports
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirect root to dashboard
    path('', lambda request: redirect('pdf_merge')),
    path('pdf/merge/', views.PDFMerge.as_view(), name='pdf_merge'),
    path('pdf/split/', views.PDFSplit.as_view(), name='pdf_split'),
    path('qrcode-generator/', views.QRCodeGenerator.as_view(), name='qrcode_generator'),
]